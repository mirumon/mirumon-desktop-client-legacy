use log4rs::{
    append::console::ConsoleAppender,
    config::{Appender, Config, Root},
    encode::pattern::PatternEncoder,
};

const LOG_PATTERN: &str = "[{d(%Y-%m-%d %H:%M:%S)} {h({l})} {t}] {m}{n}";
const APPLICATION_NAME: &str = "Mirumon Desktop";

pub fn setup_logging(log_level: log::LevelFilter) {
    log4rs::init_config(
        Config::builder()
            .appender(
                Appender::builder().build(
                    "stdout",
                    Box::new(
                        ConsoleAppender::builder()
                            .encoder(Box::new(PatternEncoder::new(LOG_PATTERN)))
                            .build(),
                    ),
                ),
            )
            .build(Root::builder().appender("stdout").build(log_level))
            .unwrap(),
    )
    .unwrap();
}

#[cfg(windows)]
pub fn setup_windows_service_logging() {
    winlog::init(APPLICATION_NAME).unwrap();
}

#[cfg(windows)]
pub fn install_windows_log() {
    winlog::try_register(APPLICATION_NAME).unwrap();
}

#[cfg(windows)]
pub fn uninstall_windows_log() {
    winlog::try_deregister(APPLICATION_NAME).unwrap();
}
