from ingestion import config


def test_paths_are_inside_project_root() -> None:
    for path in (config.RAW_DIR, config.MANUAL_RAW_DIR, config.EXPORTS_DIR, config.WAREHOUSE_PATH):
        assert path.is_relative_to(config.PROJECT_ROOT)


def test_request_interval_is_polite() -> None:
    assert config.MIN_REQUEST_INTERVAL_SECONDS >= 2.0


def test_scope_is_ordered() -> None:
    assert config.SCOPE_START < config.SCOPE_END
