//! Study lists, built once at load: for every (company, period), for "any" company per period
//! and for "LC 1–1000", the problems in new-card order. Requests walk one list instead of
//! scanning and sorting every problem.

use crate::model::{CompanyFilter, PERIOD_SLOTS, Period, Problem};

/// One problem of a list, with its rank and frequency in that list.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct ListEntry {
    /// Index into the content's problems.
    pub problem: u32,
    /// Rank in the list: the company's rank, the position for "any", the number for
    /// "LC 1–1000".
    pub rank: u32,
    /// The company's frequency, the best across companies for "any", and the best all-time
    /// frequency (or 0) for "LC 1–1000".
    pub frequency: f32,
}

/// Which list: a company (or any) and a period. [`Period::Lc1000`] ignores the company.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ListId {
    /// Whose list.
    pub company: CompanyFilter,
    /// Which period.
    pub period: Period,
}

/// Every list, flat: "LC 1–1000" first, then per period "any", then per company.
#[derive(Debug, Default)]
pub struct Lists {
    lists: Box<[Box<[ListEntry]>]>,
    companies: usize,
}

/// Where a list lives in [`Lists`], or `None` for an unknown company.
fn index(id: ListId, companies: usize) -> Option<usize> {
    let Some(slot) = id.period.slot() else {
        return Some(0);
    };
    let owner = match id.company {
        CompanyFilter::Any => 0,
        CompanyFilter::Company(c) if usize::from(c) < companies => usize::from(c) + 1,
        CompanyFilter::Company(_) => return None,
    };
    Some(1 + owner * PERIOD_SLOTS + slot)
}

impl Lists {
    /// Builds every list over `problems`, for a table of `companies` companies.
    #[must_use]
    pub fn build(problems: &[Problem], companies: usize) -> Self {
        let mut lists: Vec<Vec<ListEntry>> = vec![Vec::new(); 1 + (companies + 1) * PERIOD_SLOTS];
        let any = |slot: usize| 1 + slot;
        let company = |c: u8, slot: usize| 1 + (usize::from(c) + 1) * PERIOD_SLOTS + slot;
        for (i, p) in (0_u32..).zip(problems) {
            let entry = |rank, frequency| ListEntry {
                problem: i,
                rank,
                frequency,
            };
            if p.in_lc1000() {
                lists[0].push(entry(p.id, p.best_frequency(Period::All).unwrap_or(0.0)));
            }
            for c in &p.companies {
                for (slot, asked) in c.periods.iter().enumerate() {
                    if let Some(asked) = asked {
                        lists[company(c.company, slot)]
                            .push(entry(asked.position(), asked.frequency));
                    }
                }
            }
            for (slot, &period) in Period::COMPANY.iter().enumerate() {
                if let Some(best) = p.best_frequency(period) {
                    lists[any(slot)].push(entry(0, best));
                }
            }
        }

        let id = |e: &ListEntry| problems[e.problem as usize].id;
        for (i, list) in lists.iter_mut().enumerate() {
            if (1..=PERIOD_SLOTS).contains(&i) {
                // "Any": most frequent first, ties by number; the rank is the position.
                list.sort_by(|a, b| {
                    b.frequency
                        .total_cmp(&a.frequency)
                        .then_with(|| id(a).cmp(&id(b)))
                });
                for (rank, e) in (1..).zip(list.iter_mut()) {
                    e.rank = rank;
                }
            } else {
                list.sort_by(|a, b| a.rank.cmp(&b.rank).then_with(|| id(a).cmp(&id(b))));
            }
        }
        Self {
            lists: lists.into_iter().map(Vec::into_boxed_slice).collect(),
            companies,
        }
    }

    /// The list, in new-card order; empty for an unknown company.
    #[must_use]
    pub fn get(&self, id: ListId) -> &[ListEntry] {
        index(id, self.companies)
            .and_then(|i| self.lists.get(i))
            .map_or(&[], |list| list)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::fixtures::{GOOGLE, META, asked, classic, problem, with};

    fn ids(problems: &[Problem], list: &[ListEntry]) -> Vec<u32> {
        list.iter()
            .map(|e| problems[e.problem as usize].id)
            .collect()
    }

    fn sample() -> Vec<Problem> {
        let mut premium = classic(4);
        premium.premium = true;
        vec![
            with(problem(3), META, Period::Months6, asked(1, 90.0)),
            premium,
            with(classic(5), META, Period::Months6, asked(2, 40.0)),
            with(problem(2), GOOGLE, Period::Days30, asked(1, 70.0)),
            classic(7),
            with(classic(1200), GOOGLE, Period::All, asked(9, 5.0)),
        ]
    }

    fn list(lists: &Lists, company: CompanyFilter, period: Period) -> &[ListEntry] {
        lists.get(ListId { company, period })
    }

    #[test]
    fn company_lists_follow_the_company_rank() {
        let problems = sample();
        let lists = Lists::build(&problems, 2);
        let google = CompanyFilter::Company(GOOGLE);
        let meta = CompanyFilter::Company(META);
        assert_eq!(
            ids(&problems, list(&lists, google, Period::Months6)),
            [2, 3]
        );
        assert_eq!(ids(&problems, list(&lists, google, Period::Days30)), [2]);
        assert_eq!(ids(&problems, list(&lists, google, Period::All)), [1200]);
        assert_eq!(ids(&problems, list(&lists, meta, Period::Months6)), [3, 5]);
        let entry = list(&lists, meta, Period::Months6)[1];
        assert_eq!((entry.rank, entry.frequency), (2, 40.0));
        assert_eq!(
            list(&lists, CompanyFilter::Company(9), Period::Months6).len(),
            0
        );
    }

    #[test]
    fn any_lists_order_by_the_best_frequency() {
        let problems = sample();
        let lists = Lists::build(&problems, 2);
        let six = list(&lists, CompanyFilter::Any, Period::Months6);
        // Problem 3: best 90 (Meta); 5: 40; 2: 10 (Google).
        assert_eq!(ids(&problems, six), [3, 5, 2]);
        assert_eq!(six.iter().map(|e| e.rank).collect::<Vec<_>>(), [1, 2, 3]);
        assert_eq!(six[0].frequency, 90.0);
    }

    #[test]
    fn lc1000_takes_every_problem_up_to_1000_by_number_for_any_company() {
        let problems = sample();
        let lists = Lists::build(&problems, 2);
        for company in [CompanyFilter::Any, CompanyFilter::Company(META)] {
            let lc = list(&lists, company, Period::Lc1000);
            // Premium problem 4 included.
            assert_eq!(ids(&problems, lc), [2, 3, 4, 5, 7]);
            assert_eq!(
                lc.iter().map(|e| e.rank).collect::<Vec<_>>(),
                [2, 3, 4, 5, 7]
            );
        }
    }
}
