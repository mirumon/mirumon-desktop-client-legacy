use serde::Deserialize;

use crate::utils::{from_str, wmi_dt_to_rfc3339};

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_BaseBoard"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct MotherBoard {
    name: String,
    product: String,
    serial_number: String,
    manufacturer: String,
}

impl MotherBoard {
    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn product(&self) -> String {
        self.product.clone()
    }
    pub fn serial_number(&self) -> String {
        self.serial_number.clone()
    }
    pub fn manufacturer(&self) -> String {
        self.manufacturer.clone()
    }
}

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_Processor"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct Processor {
    name: String,
    current_clock_speed: u32,
    virtualization_firmware_enabled: bool,
    load_percentage: u16,
    number_of_cores: u32,
    number_of_enabled_core: u32,
    number_of_logical_processors: u32,
}

impl Processor {
    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn clock_speed(&self) -> u32 {
        self.current_clock_speed
    }
    pub fn virtualization_enabled(&self) -> bool {
        self.virtualization_firmware_enabled
    }
    pub fn load_percentage(&self) -> u16 {
        self.load_percentage
    }
    pub fn number_of_cores(&self) -> u32 {
        self.number_of_cores
    }
    pub fn number_of_enabled_cores(&self) -> u32 {
        self.number_of_enabled_core
    }
    pub fn number_of_logical_processors(&self) -> u32 {
        self.number_of_logical_processors
    }
}

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_VideoController"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct VideoController {
    name: String,
    current_vertical_resolution: u32,
    current_horizontal_resolution: u32,

    #[serde(deserialize_with = "wmi_dt_to_rfc3339")]
    driver_date: String,
    driver_version: String,
}

impl VideoController {
    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn vertical_resolution(&self) -> u32 {
        self.current_vertical_resolution
    }
    pub fn horizontal_resolution(&self) -> u32 {
        self.current_horizontal_resolution
    }
    pub fn driver_date(&self) -> String {
        self.driver_date.clone()
    }
    pub fn driver_version(&self) -> String {
        self.driver_version.clone()
    }
}

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_NetworkAdapterConfiguration"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct NetworkAdapterConfiguration {
    description: String,

    #[serde(rename(deserialize = "MACAddress"))]
    mac_address: Option<String>,

    #[serde(rename(deserialize = "IPAddress"))]
    ip_addresses: Option<Vec<String>>,

    #[serde(rename(deserialize = "IPEnabled"))]
    ip_enabled: bool,
}

impl NetworkAdapterConfiguration {
    pub fn description(&self) -> String {
        self.description.clone()
    }

    pub fn mac_address(&self) -> Option<String> {
        self.mac_address.clone()
    }

    pub fn ip_addresses(&self) -> Vec<String> {
        match &self.ip_addresses {
            Some(ip_addresses) => ip_addresses.clone(),
            None => vec![],
        }
    }

    pub fn ip_enabled(&self) -> bool {
        self.ip_enabled
    }
}

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_DiskDrive"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct Disk {
    model: String,
    serial_number: String,
    description: String,
    partitions: u32,

    #[serde(deserialize_with = "from_str")]
    size: u64,
}

impl Disk {
    pub fn model(&self) -> String {
        self.model.clone()
    }
    pub fn serial_number(&self) -> String {
        self.serial_number.clone()
    }
    pub fn description(&self) -> String {
        self.description.clone()
    }
    pub fn partitions(&self) -> u32 {
        self.partitions
    }
    pub fn size(&self) -> u64 {
        self.size
    }
}
