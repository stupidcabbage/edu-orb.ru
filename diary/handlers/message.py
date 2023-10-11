import jinja2


async def render_template(template_name: str, data: dict | None = None) -> str:
    if data is None:
        data = {}
    template = (await _get_template_env()).get_template(template_name)
    rendered = await template.render_async(**data)
    rendered = rendered.replace("\n", "").replace("<br>", "\n")
    del _get_template_env.template_env
    return rendered


async def _get_template_env():
    if not getattr(_get_template_env, "template_env", None):
        template_loader = jinja2.FileSystemLoader(
                searchpath=config.TEMPLATES_DIR)
        env = jinja2.Environment(
                loader=template_loader,
                trim_blocks=True,
                lstrip_blocks=True,
                autoescape=True,
                enable_async=True,
                )

        _get_template_env.template_env = env

        return _get_template_env.template_env
