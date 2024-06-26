#   Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from common_import import *


@benchmark_registry.register("adaptive_avg_pool2d")
class PaddleAdaptiveAvgPool2D(PaddleOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        adaptive_avg_pool2d = paddle.nn.AdaptiveAvgPool2D(
            output_size=config.output_size, data_format=config.data_format)
        result = adaptive_avg_pool2d(x)

        self.feed_list = [x]
        self.fetch_list = [result]
        if config.backward:
            self.append_gradients(result, [x])


@benchmark_registry.register("adaptive_avg_pool2d")
class TorchAdaptiveAvgPool2D(PytorchOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name="x", shape=config.x_shape, dtype=config.x_dtype)
        adaptive_avg_pool2d = torch.nn.AdaptiveAvgPool2d(
            output_size=config.output_size)
        result = adaptive_avg_pool2d(x)

        self.feed_list = [x]
        self.fetch_list = [result]
        if config.backward:
            self.append_gradients(result, [x])


@benchmark_registry.register("adaptive_avg_pool2d")
class TFAdaptiveAvgPool2d(TensorflowOpBenchmarkBase):
    def build_graph(self, config):
        import tensorflow_addons as tfa

        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        data_format = "channels_first"
        if config.data_format == 'NHWC':
            data_format = "channels_last"
        tf_func = tfa.layers.AdaptiveAveragePooling2D(
            output_size=config.output_size, data_format=data_format)
        out = tf_func(x)

        self.feed_list = [x]
        self.fetch_list = [out]
        if config.backward:
            self.append_gradients(out, [x])
