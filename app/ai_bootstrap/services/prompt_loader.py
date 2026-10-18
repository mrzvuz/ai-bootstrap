from pathlib import Path

import frontmatter
from jinja2 import Environment, FileSystemLoader, StrictUndefined, meta

class PromptManager:
    """Load and render prompt templates."""

    _env: Environment | None = None

    @classmethod
    def _get_env(cls, templates_dir="prompts") -> Environment:
        """Return the shared Jinja environment."""
        templates_dir = Path(__file__).parent.parent / templates_dir
        if cls._env is None:
            cls._env = Environment(
                loader=FileSystemLoader(templates_dir),
                undefined=StrictUndefined,
            )
        return cls._env

    @staticmethod
    def get_prompt(template: str, prompts_dir=None, **variables) -> str:
        """Render a named template with the supplied variables."""
        if prompts_dir is not None:
            env = Environment(
                loader=FileSystemLoader(prompts_dir),
                undefined=StrictUndefined,
            )
        else:
            env = PromptManager._get_env()
        template_path = f"{template}.j2"
        source = env.loader.get_source(env, template_path)[0]
        post = frontmatter.loads(source)
        return env.from_string(post.content).render(**variables)

    @staticmethod
    def get_template_info(template: str) -> dict:
        """Return template metadata and referenced variables."""
        env = PromptManager._get_env()
        template_path = f"{template}.j2"
        source = env.loader.get_source(env, template_path)[0]
        post = frontmatter.loads(source)

        ast = env.parse(post.content)
        variables = meta.find_undeclared_variables(ast)

        return {
            "name": template,
            "description": post.metadata.get("description", "No description provided"),
            "author": post.metadata.get("author", "Unknown"),
            "variables": list(variables),
            "frontmatter": post.metadata,
        }
