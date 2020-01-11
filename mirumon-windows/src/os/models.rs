use serde::Deserialize;

use crate::utils::wmi_dt_to_rfc3339;

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_OperatingSystem"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct OperatingSystem {
    #[serde(rename(deserialize = "Caption"))]
    name: String,
    version: String,
    os_architecture: String,
    serial_number: String,
    number_of_users: u32,

    #[serde(deserialize_with = "wmi_dt_to_rfc3339")]
    install_date: String,
}

impl OperatingSystem {
    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn version(&self) -> String {
        self.version.clone()
    }
    pub fn os_architecture(&self) -> String {
        self.os_architecture.clone()
    }
    pub fn serial_number(&self) -> String {
        self.serial_number.clone()
    }
    pub fn number_of_users(&self) -> u32 {
        self.number_of_users
    }
    pub fn install_date(&self) -> String {
        self.install_date.clone()
    }
}

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_ComputerSystem"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct ComputerSystem {
    name: String,
    user_name: String,
    workgroup: String,
    domain: String,
    part_of_domain: bool,
}

impl ComputerSystem {
    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn user_name(&self) -> String {
        self.user_name.clone()
    }
    pub fn workgroup(&self) -> String {
        self.workgroup.clone()
    }
    pub fn domain(&self) -> String {
        self.domain.clone()
    }
    pub fn part_of_domain(&self) -> bool {
        self.part_of_domain
    }
}

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_UserAccount"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct UserAccount {
    name: String,
    domain: String,
    full_name: String,
}

impl UserAccount {
    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn domain(&self) -> String {
        self.domain.clone()
    }
    pub fn full_name(&self) -> String {
        self.full_name.clone()
    }
}
