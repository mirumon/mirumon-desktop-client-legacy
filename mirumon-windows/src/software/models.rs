use serde::Deserialize;

#[derive(Deserialize)]
#[serde(rename(deserialize = "Win32_InstalledWin32Program"))]
#[serde(rename_all(deserialize = "PascalCase"))]
pub struct Program {
    name: String,
    vendor: String,
    version: String,
}

impl Program {
    pub fn name(&self) -> String {
        self.name.clone()
    }
    pub fn vendor(&self) -> String {
        self.vendor.clone()
    }
    pub fn version(&self) -> String {
        self.version.clone()
    }
}
