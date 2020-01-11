use crate::hardware::models::{
    Disk, MotherBoard, NetworkAdapterConfiguration, Processor, VideoController,
};
use crate::manager::{MirumonManager, MirumonService};
use crate::utils::{wmi_first, wmi_list};
use mac_address::get_mac_address;

pub struct HardwareService<'a> {
    manager: &'a MirumonManager,
}

impl<'a> MirumonService<'a> for HardwareService<'a> {
    fn new(manager: &'a MirumonManager) -> Self {
        Self { manager }
    }

    fn manager(&self) -> &'a MirumonManager {
        self.manager
    }
}

impl HardwareService<'_> {
    pub fn mac_address(&self) -> String {
        match get_mac_address() {
            Ok(Some(addr)) => addr.to_string(),
            _ => panic!("error while getting MAC address from OS"),
        }
    }

    pub fn motherboard(&self) -> MotherBoard {
        wmi_first(self)
    }

    pub fn processors(&self) -> Vec<Processor> {
        wmi_list(self)
    }

    pub fn graphic_cards(&self) -> Vec<VideoController> {
        wmi_list(self)
    }

    pub fn network_adapters_configurations(&self) -> Vec<NetworkAdapterConfiguration> {
        wmi_list(self)
            .into_iter()
            .filter(|config: &NetworkAdapterConfiguration| config.ip_enabled())
            .collect()
    }

    pub fn physical_disks(&self) -> Vec<Disk> {
        wmi_list(self)
    }
}
