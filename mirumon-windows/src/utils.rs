use crate::manager::MirumonService;
use serde::{de, Deserialize, Deserializer};
use std::fmt::Display;
use std::str::FromStr;
use wmi::WMIDateTime;

pub fn wmi_dt_to_rfc3339<'de, D>(deserializer: D) -> Result<String, D::Error>
where
    D: Deserializer<'de>,
{
    let s = String::deserialize(deserializer)?;
    let dt = WMIDateTime::from_str(s.as_str()).map_err(de::Error::custom)?;
    Ok(dt.0.to_rfc3339())
}

pub fn from_str<'de, T, D>(deserializer: D) -> Result<T, D::Error>
where
    T: FromStr,
    T::Err: Display,
    D: Deserializer<'de>,
{
    let s = String::deserialize(deserializer)?;
    T::from_str(&s).map_err(de::Error::custom)
}

pub fn wmi_first<'a, T>(service: &'a impl MirumonService<'a>) -> T
where
    T: de::DeserializeOwned,
{
    service
        .manager()
        .wmi::<T>()
        .unwrap_or_else(|err| {
            panic!(
                "error getting list of items of type '{}' using WMI: {}",
                std::any::type_name::<T>(),
                err
            )
        })
        .drain(0..)
        .next()
        .unwrap()
}

pub fn wmi_list<'a, T>(service: &'a impl MirumonService<'a>) -> Vec<T>
where
    T: de::DeserializeOwned,
{
    service.manager().wmi::<T>().unwrap_or_else(|err| {
        panic!(
            "error getting list of items of type '{}' using WMI: {}",
            std::any::type_name::<T>(),
            err
        )
    })
}
