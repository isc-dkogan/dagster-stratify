from dagster import Definitions, load_assets_from_modules, AssetSelection, define_asset_job, ScheduleDefinition

from . import assets

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
)

config_validation = AssetSelection.keys("config_validation")
computations = AssetSelection.keys("computations")

config_validation_job = define_asset_job(
  name="config_validation_job",
  selection=config_validation,
)

computations_job = define_asset_job(
  name="computations_job",
  selection=computations,
)

config_validation_schedule = ScheduleDefinition(
    job=config_validation_job,
    cron_schedule="55 20 * * 1-5",
)

computations_schedule = ScheduleDefinition(
    job=computations_job,
    cron_schedule="6 15 * * 1-5",
)

defs = Definitions(
    assets=all_assets,
    jobs=[config_validation_job, computations_job],
    schedules=[config_validation_schedule, computations_schedule]
)
