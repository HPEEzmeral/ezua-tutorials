from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field, FileSource, ValueType
from feast.types import Float32, Float64, Int64


Id = Entity(name="Id", join_keys=["Id"])

train_source = FileSource(
    name="train",
    path="/mnt/user/data/HousingPriceRegression/train.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

train_view1 = FeatureView(
    name="train_view1",
    entities=[Id],
    schema=[
        Field(name='MSSubClass', dtype=Float32),
        Field(name='MSZoning', dtype=Float32),
        Field(name='LotFrontage', dtype=Float32),
        Field(name='LotArea', dtype=Float32),
        Field(name='LotShape', dtype=Float32),
        Field(name='LotConfig', dtype=Float32),
        Field(name='Neighborhood', dtype=Float32),
        Field(name='Condition1', dtype=Float32),
        Field(name='OverallQual', dtype=Float32),
        Field(name='OverallCond', dtype=Float32),
        Field(name='YearBuilt', dtype=Float32),
        Field(name='YearRemodAdd', dtype=Float32),
        Field(name='RoofStyle', dtype=Float32),
        Field(name='Exterior1st', dtype=Float32),
        Field(name='MasVnrType', dtype=Float32),
        Field(name='ExterQual', dtype=Float32),
        Field(name='Foundation', dtype=Float32),
        Field(name='BsmtQual', dtype=Float32),
        Field(name='BsmtExposure', dtype=Float32),
        Field(name='BsmtFinSF1', dtype=Float32),
        Field(name='BsmtFinSF2', dtype=Float32),
        Field(name='TotalBsmtSF', dtype=Float32),
        Field(name='HeatingQC', dtype=Float32),
        Field(name='CentralAir', dtype=Float32),
        Field(name='GrLivArea', dtype=Float32),
        Field(name='BsmtFullBath', dtype=Float32),
        Field(name='FullBath', dtype=Float32),
        Field(name='HalfBath', dtype=Float32),
        Field(name='KitchenQual', dtype=Float32),
        Field(name='TotRmsAbvGrd', dtype=Float32),
        Field(name='Functional', dtype=Float32),
        Field(name='Fireplaces', dtype=Float32),
        Field(name='FireplaceQu', dtype=Float32),
        Field(name='GarageFinish', dtype=Float32),
        Field(name='GarageCars', dtype=Float32),
        Field(name='GarageArea', dtype=Float32),
        Field(name='GarageCond', dtype=Float32),
        Field(name='PavedDrive', dtype=Float32),
        Field(name='ScreenPorch', dtype=Float32),
        Field(name='YrSold', dtype=Float32),
        Field(name='SaleType', dtype=Float32),
        Field(name='SaleCondition', dtype=Float32),
        Field(name='SalePrice', dtype=Float32)
    ],
    online=True,
    source=train_source,
    tags={"team": "train model"},
    ttl=timedelta(days=1),
)


train_service1 = FeatureService(
    name="train_service1", features=[train_view1]
)

train_view2 = FeatureView(
    name="train_view2",
    entities=[Id],
    schema=[
        Field(name='MSSubClass',dtype=Float32),
        Field(name='MSZoning',dtype=Float32),
        Field(name='LotConfig',dtype=Float32),
        Field(name='Neighborhood',dtype=Float32),
        Field(name='OverallQual',dtype=Float32),
        Field(name='YearRemodAdd',dtype=Float32),
        Field(name='MasVnrType',dtype=Float32),
        Field(name='BsmtQual',dtype=Float32),
        Field(name='BsmtExposure',dtype=Float32),
        Field(name='BsmtFinSF1',dtype=Float32),
        Field(name='CentralAir',dtype=Float32),
        Field(name='FirstFlrSF',dtype=Float32),
        Field(name='GrLivArea',dtype=Float32),
        Field(name='BsmtFullBath',dtype=Float32),
        Field(name='KitchenQual',dtype=Float32),
        Field(name='FireplaceQu',dtype=Float32),
        Field(name='GarageType',dtype=Float32),
        Field(name='GarageFinish',dtype=Float32),
        Field(name='GarageArea',dtype=Float32),
        Field(name='PavedDrive',dtype=Float32),
        Field(name='SaleCondition', dtype=Float32),
        Field(name='SalePrice', dtype=Float32)
    ],
    online=True,
    source=train_source,
    tags={},
    ttl=timedelta(days=1),
)


train_service2 = FeatureService(
    name="train_service2", features=[train_view2]
)

train_view3 = FeatureView(
    name="train_view3",
    entities=[Id],
    schema=[
        Field(name='Neighborhood',  dtype=Float32),
        Field(name='OverallQual',  dtype=Float32),
        Field(name='YearRemodAdd',  dtype=Float32),
        Field(name='MasVnrType',  dtype=Float32),
        Field(name='BsmtQual',  dtype=Float32),
        Field(name='BsmtExposure',  dtype=Float32),
        Field(name='CentralAir',  dtype=Float32),
        Field(name='FirstFlrSF',  dtype=Float32),
        Field(name='GrLivArea',  dtype=Float32),
        Field(name='KitchenQual',  dtype=Float32),
        Field(name='FireplaceQu',  dtype=Float32),
        Field(name='GarageType',  dtype=Float32),
        Field(name='GarageFinish',  dtype=Float32),
        Field(name='GarageArea',  dtype=Float32),
        Field(name='SalePrice', dtype=Float32)
    ],
    online=True,
    source=train_source,
    tags={},
    ttl=timedelta(days=1),
)


train_service3 = FeatureService(
    name="train_service3", features=[train_view3]
)

test_source = FileSource(
    name="test",
    path="/mnt/user/data/HousingPriceRegression/test.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)


test_view1 = FeatureView(
    name="test_view1",
    entities=[Id],
    schema=[
        Field(name='MSSubClass', dtype=Float32),
        Field(name='MSZoning', dtype=Float32),
        Field(name='LotFrontage', dtype=Float32),
        Field(name='LotArea', dtype=Float32),
        Field(name='LotShape', dtype=Float32),
        Field(name='LotConfig', dtype=Float32),
        Field(name='Neighborhood', dtype=Float32),
        Field(name='Condition1', dtype=Float32),
        Field(name='OverallQual', dtype=Float32),
        Field(name='OverallCond', dtype=Float32),
        Field(name='YearBuilt', dtype=Float32),
        Field(name='YearRemodAdd', dtype=Float32),
        Field(name='RoofStyle', dtype=Float32),
        Field(name='Exterior1st', dtype=Float32),
        Field(name='MasVnrType', dtype=Float32),
        Field(name='ExterQual', dtype=Float32),
        Field(name='Foundation', dtype=Float32),
        Field(name='BsmtQual', dtype=Float32),
        Field(name='BsmtExposure', dtype=Float32),
        Field(name='BsmtFinSF1', dtype=Float32),
        Field(name='BsmtFinSF2', dtype=Float32),
        Field(name='TotalBsmtSF', dtype=Float32),
        Field(name='HeatingQC', dtype=Float32),
        Field(name='CentralAir', dtype=Float32),
        Field(name='GrLivArea', dtype=Float32),
        Field(name='BsmtFullBath', dtype=Float32),
        Field(name='FullBath', dtype=Float32),
        Field(name='HalfBath', dtype=Float32),
        Field(name='KitchenQual', dtype=Float32),
        Field(name='TotRmsAbvGrd', dtype=Float32),
        Field(name='Functional', dtype=Float32),
        Field(name='Fireplaces', dtype=Float32),
        Field(name='FireplaceQu', dtype=Float32),
        Field(name='GarageFinish', dtype=Float32),
        Field(name='GarageCars', dtype=Float32),
        Field(name='GarageArea', dtype=Float32),
        Field(name='GarageCond', dtype=Float32),
        Field(name='PavedDrive', dtype=Float32),
        Field(name='ScreenPorch', dtype=Float32),
        Field(name='YrSold', dtype=Float32),
        Field(name='SaleType', dtype=Float32),
        Field(name='SaleCondition', dtype=Float32)
    ],
    online=True,
    source=test_source,
    tags={},
    ttl=timedelta(days=1),
)


test_service1 = FeatureService(
    name="test_service1", features=[test_view1]
)


test_view2 = FeatureView(
    name="test_view2",
    entities=[Id],
    schema=[
        Field(name='MSSubClass',dtype=Float32),
        Field(name='MSZoning',dtype=Float32),
        Field(name='LotConfig',dtype=Float32),
        Field(name='Neighborhood',dtype=Float32),
        Field(name='OverallQual',dtype=Float32),
        Field(name='YearRemodAdd',dtype=Float32),
        Field(name='MasVnrType',dtype=Float32),
        Field(name='BsmtQual',dtype=Float32),
        Field(name='BsmtExposure',dtype=Float32),
        Field(name='BsmtFinSF1',dtype=Float32),
        Field(name='CentralAir',dtype=Float32),
        Field(name='FirstFlrSF',dtype=Float32),
        Field(name='GrLivArea',dtype=Float32),
        Field(name='BsmtFullBath',dtype=Float32),
        Field(name='KitchenQual',dtype=Float32),
        Field(name='FireplaceQu',dtype=Float32),
        Field(name='GarageType',dtype=Float32),
        Field(name='GarageFinish',dtype=Float32),
        Field(name='GarageArea',dtype=Float32),
        Field(name='PavedDrive',dtype=Float32),
        Field(name='SaleCondition', dtype=Float32)
    ],
    online=True,
    source=test_source,
    tags={},
    ttl=timedelta(days=1),
)


test_service2 = FeatureService(
    name="test_service2", features=[test_view2]
)



test_view3 = FeatureView(
    name="test_view3",
    entities=[Id],
    schema=[
        Field(name='Neighborhood',  dtype=Float32),
        Field(name='OverallQual',  dtype=Float32),
        Field(name='YearRemodAdd',  dtype=Float32),
        Field(name='MasVnrType',  dtype=Float32),
        Field(name='BsmtQual',  dtype=Float32),
        Field(name='BsmtExposure',  dtype=Float32),
        Field(name='CentralAir',  dtype=Float32),
        Field(name='FirstFlrSF',  dtype=Float32),
        Field(name='GrLivArea',  dtype=Float32),
        Field(name='KitchenQual',  dtype=Float32),
        Field(name='FireplaceQu',  dtype=Float32),
        Field(name='GarageType',  dtype=Float32),
        Field(name='GarageFinish',  dtype=Float32),
        Field(name='GarageArea',  dtype=Float32)
    ],
    online=True,
    source=test_source,
    tags={},
    ttl=timedelta(days=1),
)


test_service3 = FeatureService(
    name="test_service3", features=[test_view3]
)
