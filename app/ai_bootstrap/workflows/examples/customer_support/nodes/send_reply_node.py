import logging

from ai_bootstrap.core.nodes.base import Node
from ai_bootstrap.core.task import TaskContext
from ai_bootstrap.workflows.examples.customer_support.nodes.generate_response_node import GenerateResponseNode


class SendReplyNode(Node):
    async def process(self, task_context: TaskContext) -> TaskContext:
        logging.info("Sending reply:")
        generate_response_node: GenerateResponseNode.OutputType = self.get_output(
            GenerateResponseNode
        )
        logging.info(generate_response_node.response)
        return task_context
