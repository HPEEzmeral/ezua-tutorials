# Copyright 2023 The KServe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    KServe

    Python SDK for KServe  # noqa: E501

    The version of the OpenAPI document: v0.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kserve.configuration import Configuration


class V1alpha1TrainedModelSpec(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'inference_service': 'str',
        'model': 'V1alpha1ModelSpec'
    }

    attribute_map = {
        'inference_service': 'inferenceService',
        'model': 'model'
    }

    def __init__(self, inference_service='', model=None, local_vars_configuration=None):  # noqa: E501
        """V1alpha1TrainedModelSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._inference_service = None
        self._model = None
        self.discriminator = None

        self.inference_service = inference_service
        self.model = model

    @property
    def inference_service(self):
        """Gets the inference_service of this V1alpha1TrainedModelSpec.  # noqa: E501

        parent inference service to deploy to  # noqa: E501

        :return: The inference_service of this V1alpha1TrainedModelSpec.  # noqa: E501
        :rtype: str
        """
        return self._inference_service

    @inference_service.setter
    def inference_service(self, inference_service):
        """Sets the inference_service of this V1alpha1TrainedModelSpec.

        parent inference service to deploy to  # noqa: E501

        :param inference_service: The inference_service of this V1alpha1TrainedModelSpec.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and inference_service is None:  # noqa: E501
            raise ValueError("Invalid value for `inference_service`, must not be `None`")  # noqa: E501

        self._inference_service = inference_service

    @property
    def model(self):
        """Gets the model of this V1alpha1TrainedModelSpec.  # noqa: E501


        :return: The model of this V1alpha1TrainedModelSpec.  # noqa: E501
        :rtype: V1alpha1ModelSpec
        """
        return self._model

    @model.setter
    def model(self, model):
        """Sets the model of this V1alpha1TrainedModelSpec.


        :param model: The model of this V1alpha1TrainedModelSpec.  # noqa: E501
        :type: V1alpha1ModelSpec
        """
        if self.local_vars_configuration.client_side_validation and model is None:  # noqa: E501
            raise ValueError("Invalid value for `model`, must not be `None`")  # noqa: E501

        self._model = model

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1alpha1TrainedModelSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1alpha1TrainedModelSpec):
            return True

        return self.to_dict() != other.to_dict()
