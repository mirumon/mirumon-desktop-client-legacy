use crate::cli::ApplicationConfig;
use mirumon_desktop::logging;

mod cli;

fn main() {
    let config = cli::config();

    setup_logs(config);
}

fn setup_logs(config: &ApplicationConfig) {
    if config.install_service {
        #[cfg(windows)]
        logging::install_windows_log();
    }
    if config.uninstall_service {
        #[cfg(windows)]
        logging::uninstall_windows_log();
    }

    if config.run_as_service {
        #[cfg(windows)]
        logging::setup_windows_service_logging();
    } else {
        logging::setup_logging(config.logging_level);
    }
}
