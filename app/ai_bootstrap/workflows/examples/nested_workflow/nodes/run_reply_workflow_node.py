from pydantic import BaseModel

from ai_bootstrap.core.nodes.base import Node
from ai_bootstrap.core.task import TaskContext
from ai_bootstrap.workflows.examples.nested_workflow.reply_workflow import (
    ReplyDraftWorkflow,
)


class RunReplyWorkflowNode(Node):
    class OutputType(BaseModel):
        delegated: bool
        workflow: str

    async def process(self, task_context: TaskContext) -> TaskContext:
        await ReplyDraftWorkflow().run_async(context=task_context)
        self.save_output(self.OutputType(delegated=True, workflow="ReplyDraftWorkflow"))
        return task_context
