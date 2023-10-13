from pathlib import Path
from datetime import timedelta

import pandas as pd
from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    PushSource,
    RequestSource,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int64


DATA_PATH = Path("dataset/driver_stats.parquet")

__all__ = ["driver",
           "driver_stats_source",
           "driver_stats_feature_view",
           "transformed_stats",
           "driver_stats_push_source",
           "driver_activity",
           "driver_stats_fresh_feature_view"]


# Define an entity for the driver.
# You can think of an entity as a primary key used to fetch features.
driver = Entity(name="driver", join_keys=["driver_id"])

# Read data from parquet files. Parquet is convenient for development mode.
# For production, you can use your favorite DWH, such as BigQuery.
# See Feast documentation for more info.
driver_stats_source = FileSource(
    name="driver_hourly_stats_source",
    path=str(DATA_PATH),
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

# The dataset includes a `driver_id`, a timestamp and other feature columns.
# Here we define a Feature View to serve this data to our model online.
driver_stats_feature_view = FeatureView(
    # The unique name of this feature view.
    # Two feature views in a single project cannot have the same name.
    name="driver_hourly_stats",
    entities=[driver],
    ttl=timedelta(days=1),
    # The list of features defined below define the db schema.
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64,
              description="Average daily trips"),
    ],
    online=True,
    source=driver_stats_source,
    tags={"team": "driver_performance"},
)

# Defines a way to push data (available offline, online or both) into Feast.
driver_stats_push_source = PushSource(
    name="driver_stats_push_source",
    batch_source=driver_stats_source,
)

# Define an on demand feature view which can generate new features based on
# existing feature views and RequestSource features.
@on_demand_feature_view(
    sources=[driver_stats_feature_view],
    schema=[
        Field(name="conv_plus_trips", dtype=Float64),
        Field(name="acc_plus_trips", dtype=Float64)
    ],
)
def transformed_stats(inputs: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df["conv_plus_trips"] = inputs["conv_rate"] * inputs["avg_daily_trips"]
    df["acc_plus_trips"] = inputs["acc_rate"] * inputs["avg_daily_trips"]
    return df

driver_activity = FeatureService(
    name="driver_activity", features=[driver_stats_feature_view,
                                      transformed_stats]
)

# Defines a slightly modified version of the feature view from above, where the
# source has been changed to the push source.
# This allows fresh features to be directly pushed to the online store.
driver_stats_fresh_feature_view = FeatureView(
    name="driver_hourly_stats_fresh",
    entities=[driver],
    ttl=timedelta(days=1),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    online=True,
    source=driver_stats_push_source,  # Changed from above
    tags={"team": "driver_performance"},
)
