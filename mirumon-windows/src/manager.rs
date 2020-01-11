use wmi::{COMLibrary, WMIConnection};

use crate::error::Error;
use serde::de;

pub struct MirumonManager {
    wmi_connection: WMIConnection,
}

pub trait MirumonService<'a> {
    fn new(manager: &'a MirumonManager) -> Self;

    fn manager(&self) -> &'a MirumonManager;
}

impl<'a> MirumonManager {
    pub fn new() -> Result<Self, Error> {
        let com_con = COMLibrary::new()?;
        let wmi_con = WMIConnection::new(com_con.into())?;
        Ok(Self {
            wmi_connection: wmi_con,
        })
    }

    pub fn wmi<T>(&self) -> Result<Vec<T>, Error>
    where
        T: de::DeserializeOwned,
    {
        Ok(self.wmi_connection.query::<T>()?)
    }

    pub fn service<T: MirumonService<'a>>(&'a self) -> T {
        T::new(self)
    }
}
