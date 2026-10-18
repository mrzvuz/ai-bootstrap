from launchpad.core.nodes.agent import AgentNode, AgentConfig, ModelProvider
from launchpad.core.task import TaskContext
from launchpad.workflows.examples.langfuse_tracing.schema import LangfuseTracingEventSchema


class ContextSummaryResult(AgentNode):
    def get_agent_config(self) -> AgentConfig:
        return AgentConfig(
            instructions="Summarize the comment concisely.",
            output_type=self.OutputType,
            deps_type=LangfuseTracingEventSchema,
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-5.4-mini",
            instrument=True,
        )

    class OutputType(AgentNode.OutputType):
        comment_id: str
        summary: str

    async def process(self, task_context: TaskContext) -> TaskContext:
        event: LangfuseTracingEventSchema = task_context.event

        result = await self.agent.run(user_prompt=event.model_dump_json())

        self.save_output(result.output)

        return task_context
