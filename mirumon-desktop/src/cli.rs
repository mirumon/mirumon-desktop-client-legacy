use clap::{crate_authors, crate_description, crate_version, value_t_or_exit, App, Arg};
use log;

pub struct ApplicationConfig {
    pub logging_level: log::LevelFilter,
    pub server_url: String,
    pub reconnect_delay: u32,
    pub reconnect_attempts: u32,
    pub install_service: bool,
    pub uninstall_service: bool,
    pub run_as_service: bool,
}

pub fn config() -> &'static ApplicationConfig {
    lazy_static::lazy_static! {
        static ref CONFIG: ApplicationConfig = ApplicationConfig::new();
    }
    &*CONFIG
}

impl ApplicationConfig {
    fn new() -> Self {
        let app = App::new("Mirumon Desktop Service")
            .version(crate_version!())
            .author(crate_authors!())
            .about(crate_description!())
            .arg(
                Arg::with_name("reconnect_delay")
                    .long("reconnect-delay")
                    .value_name("RECONNECT_DELAY")
                    .help("Delay in seconds between attempts to connect to mirumon backend")
                    .takes_value(true)
                    .default_value("5"),
            )
            .arg(
                Arg::with_name("reconnect_attempts")
                    .long("reconnect-attempts")
                    .value_name("RECONNECT_ATTEMPTS")
                    .help("Max attempts to connect to mirumon backend before exiting with error")
                    .takes_value(true)
                    .default_value("10"),
            )
            .arg(
                Arg::with_name("v")
                    .short("v")
                    .multiple(true)
                    .help("Logging level verbosity"),
            );

        let server_arg = Arg::with_name("server_url")
            .short("u")
            .long("url")
            .value_name("URL")
            .help("URL for Mirumon backend installation")
            .takes_value(true);
        let matches = if cfg!(windows) {
            app.arg(
                Arg::with_name("install_service")
                    .long("install-service")
                    .help(
                    "Install application as windows service, requires Administrator permissions",
                ),
            ).arg(
                Arg::with_name("uninstall_service")
                    .long("uninstall-service")
                    .help("Uninstall application from windows services, requires Administrator permissions")
                    .conflicts_with("install_service")
            )
            .arg(
                Arg::with_name("run_as_service")
                    .long("run-as-service")
                    .help("Run application as windows service")
                    .conflicts_with_all(&["install_service", "uninstall_service"]),
            )
            .arg(server_arg.required_unless("install_service"))
        } else {
            app.arg(server_arg)
        }
        .get_matches();

        let server_url = matches.value_of("server_url").unwrap_or("").to_string();
        let reconnect_delay: u32 = value_t_or_exit!(matches.value_of("reconnect_delay"), u32);
        let reconnect_attempts: u32 = value_t_or_exit!(matches.value_of("reconnect_attempts"), u32);
        let install_service = matches.is_present("install_service");
        let uninstall_service = matches.is_present("uninstall_service");
        let run_as_service = matches.is_present("run_as_service");

        let logging_level = match matches.occurrences_of("v") {
            0 => log::LevelFilter::Info,
            1 => log::LevelFilter::Debug,
            _ => log::LevelFilter::Trace,
        };

        ApplicationConfig {
            logging_level,
            server_url,
            reconnect_delay,
            reconnect_attempts,
            install_service,
            uninstall_service,
            run_as_service,
        }
    }
}
