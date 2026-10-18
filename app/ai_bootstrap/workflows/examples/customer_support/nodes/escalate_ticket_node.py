import logging

from ai_bootstrap.core.nodes.base import Node
from ai_bootstrap.core.task import TaskContext


class EscalateTicketNode(Node):
    async def process(self, task_context: TaskContext) -> TaskContext:
        logging.info("Escalating ticket")
        return task_context
