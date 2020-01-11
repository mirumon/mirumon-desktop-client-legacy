use crate::error::Error;
use crate::manager::{MirumonManager, MirumonService};
use crate::software::models::Program;

pub struct SoftwareService<'a> {
    manager: &'a MirumonManager,
}

impl<'a> MirumonService<'a> for SoftwareService<'a> {
    fn new(manager: &'a MirumonManager) -> Self {
        Self { manager }
    }

    fn manager(&self) -> &'a MirumonManager {
        self.manager
    }
}

impl SoftwareService<'_> {
    pub fn installed_programs(&self) -> Result<Vec<Program>, Error> {
        self.manager.wmi::<Program>()
    }
}
