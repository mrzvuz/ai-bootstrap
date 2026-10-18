import logging

from ai_bootstrap.core.nodes.base import Node
from ai_bootstrap.core.task import TaskContext


class ProcessInvoiceNode(Node):
    async def process(self, task_context: TaskContext) -> TaskContext:
        logging.info("Processing invoice")
        return task_context
