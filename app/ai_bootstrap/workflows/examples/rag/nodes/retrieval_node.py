from ai_bootstrap.core.nodes.base import Node
from ai_bootstrap.core.task import TaskContext
from ai_bootstrap.workflows.examples.rag.services import PgvectorRAGService, RetrievalResults
from ai_bootstrap.workflows.examples.rag.schema import RagExampleEventSchema


class RetrievalNode(Node):
    class OutputType(Node.OutputType):
        results: RetrievalResults

    async def process(self, task_context: TaskContext) -> TaskContext:
        rag_service = PgvectorRAGService()
        event: RagExampleEventSchema = task_context.event
        embedding = rag_service.get_embedding(event.query)

        results = rag_service.collection.query(
            data=embedding,
            limit=3,
            measure="cosine_distance",
            include_value=False,
            include_metadata=True,
        )
        self.save_output(self.OutputType(results=rag_service.parse_results(results)))
        rag_service.disconnect()

        return task_context
