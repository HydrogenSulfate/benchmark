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


@benchmark_registry.register("diag")
class DiagConfig(APIConfig):
    def __init__(self):
        super(DiagConfig, self).__init__("diag")

    def init_from_json(self, filename, config_id=0, unknown_dim=16):
        super(DiagConfig, self).init_from_json(filename, config_id,
                                               unknown_dim)

        if self.padding_value != 0:
            self.run_torch = False


@benchmark_registry.register("diag")
class PaddleDiag(PaddleOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        result = paddle.diag(
            x=x, offset=config.offset, padding_value=config.padding_value)

        self.feed_list = [x]
        self.fetch_list = [result]


@benchmark_registry.register("diag")
class TorchDiag(PytorchOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        result = torch.diag(input=x, diagonal=config.offset)

        self.feed_list = [x]
        self.fetch_list = [result]


@benchmark_registry.register("diag")
class TFDiag(TensorflowOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        result = tf.linalg.diag(
            diagonal=x, k=config.offset, padding_value=config.padding_value)

        self.feed_list = [x]
        self.fetch_list = [result]
