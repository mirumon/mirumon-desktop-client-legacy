use crate::error::Error;
use crate::manager::{MirumonManager, MirumonService};
use crate::os::models::{ComputerSystem, OperatingSystem, UserAccount};
use crate::utils::{wmi_first, wmi_list};
use system_shutdown::shutdown;
use wake_on_lan;

pub struct OSService<'a> {
    manager: &'a MirumonManager,
}

impl<'a> MirumonService<'a> for OSService<'a> {
    fn new(manager: &'a MirumonManager) -> Self {
        Self { manager }
    }

    fn manager(&self) -> &'a MirumonManager {
        self.manager
    }
}

impl OSService<'_> {
    pub fn operation_systems(&self) -> Vec<OperatingSystem> {
        wmi_list(self)
    }

    pub fn computer_system(&self) -> ComputerSystem {
        wmi_first(self)
    }

    pub fn current_user(&self) -> Option<UserAccount> {
        let system = self.computer_system();
        wmi_list(self).into_iter().find(|user: &UserAccount| {
            format!(r"{}\{}", user.domain(), user.name()) == system.user_name()
        })
    }

    pub fn shutdown_computer(&self) -> Result<(), Error> {
        shutdown().map_err(Error::from)
    }

    pub fn wake_computer(&self, mac_address: [u8; 6]) -> Result<(), Error> {
        Ok(wake_on_lan::MagicPacket::new(&mac_address).send()?)
    }
}
