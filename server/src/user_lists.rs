//! The learner's own problem lists: hand-picked problems in the order they were added, under
//! a name. A plan can walk one instead of a company list (`Plan::user_list`), with the same
//! filters, status and order.

use crate::content::Content;
use crate::lists::ListEntry;

/// One of the learner's lists, resolved against the content.
#[derive(Debug, Clone, PartialEq)]
pub struct UserList {
    /// Its id (`user_lists.id`).
    pub id: i64,
    /// Its name.
    pub name: String,
    /// Its problems' slugs, in list order, as stored (a slug the content no longer has stays).
    pub slugs: Vec<String>,
    /// Its known problems in list order, ranked 1, 2, 3, ...
    pub entries: Box<[ListEntry]>,
}

impl UserList {
    /// A stored list, its slugs resolved against the content.
    #[must_use]
    pub fn new(content: &Content, id: i64, name: String, slugs: Vec<String>) -> Self {
        let entries = slugs
            .iter()
            .filter_map(|slug| content.problem_index(slug))
            .zip(1..)
            .map(|(problem, rank)| ListEntry {
                problem,
                rank,
                frequency: 0.0,
            })
            .collect();
        Self {
            id,
            name,
            slugs,
            entries,
        }
    }
}

/// Every list of the learner, newest first.
#[derive(Debug, Clone, Default, PartialEq)]
pub struct UserLists(Vec<UserList>);

impl UserLists {
    /// The lists, newest first.
    #[must_use]
    pub const fn new(lists: Vec<UserList>) -> Self {
        Self(lists)
    }

    /// The list with this id.
    #[must_use]
    pub fn get(&self, id: i64) -> Option<&UserList> {
        self.0.iter().find(|list| list.id == id)
    }

    /// Every list, newest first.
    #[must_use]
    pub fn all(&self) -> &[UserList] {
        &self.0
    }

    /// The entries of a list; none for an unknown one (deleted, say).
    #[must_use]
    pub fn entries(&self, id: i64) -> &[ListEntry] {
        self.get(id).map_or(&[], |list| &list.entries)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    use crate::model::fixtures::{companies, problem};

    #[test]
    fn ranks_known_problems_in_list_order_and_keeps_every_slug() {
        let content = Content::new(companies(), vec![problem(1), problem(2)], HashMap::new());
        let list = UserList::new(
            &content,
            7,
            "Mine".into(),
            vec!["p2".into(), "gone".into(), "p1".into()],
        );
        let ranked: Vec<(u32, u32)> = list
            .entries
            .iter()
            .map(|e| (content.problem_at(e).id, e.rank))
            .collect();
        assert_eq!(ranked, [(2, 1), (1, 2)]);
        assert_eq!(list.slugs.len(), 3);
        let lists = UserLists::new(vec![list]);
        assert_eq!(lists.entries(7).len(), 2);
        assert!(lists.entries(8).is_empty());
    }
}
