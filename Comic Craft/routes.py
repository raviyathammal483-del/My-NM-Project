from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from app.config import settings

from app.demo_data import (
    demo_outline,
    demo_story,
)

from app.exporters import save_pdf

from app.gemini_flash import (
    generate_outline,
)

from app.gemini_pro import (
    generate_story,
)

from app.image_generator import (
    generate_image,
    generate_image_from_prompt,
)

from app.layout_builder import (
    build_comic_layout,
)

from app.schemas import (
    PromptRequest,
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


def create_prompt_request(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
):

    return PromptRequest(

        story_prompt=story_prompt,

        character_name=character_name,

        setting=setting,

        tone=tone,

        art_style=art_style,
    )


def create_comic(
    request: PromptRequest
):

    # --------------------------------
    # DEMO MODE
    # --------------------------------

    if not settings.gemini_api_key:

        outline = demo_outline(

            request.story_prompt,

            request.character_name,

            request.setting,

            request.tone,

            request.art_style,
        )

        story = demo_story(
            outline
        )

    # --------------------------------
    # REAL GEMINI MODE
    # --------------------------------

    else:

        outline = generate_outline(
            request
        )

        story = generate_story(
            request,
            outline
        )

    # --------------------------------
    # IMAGE GENERATION
    # --------------------------------

    image_paths = []

    for panel in outline:

        image_path = generate_image(

            panel["image_prompt"],

            panel["panel_number"],
        )

        image_paths.append(
            image_path
        )

    # --------------------------------
    # BUILD LAYOUT
    # --------------------------------

    layout = build_comic_layout(

        outline,

        story,

        image_paths,
    )

    # --------------------------------
    # EXPORT PDF
    # --------------------------------

    pdf_path = save_pdf(
        layout
    )

    return layout, pdf_path


# ====================================
# HOME PAGE
# ====================================

@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={
            "title": "ComicCraft"
        },
    )


# ====================================
# HTML GENERATION ROUTE
# ====================================

@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(

    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):

    try:

        payload = create_prompt_request(

            story_prompt,

            character_name,

            setting,

            tone,

            art_style,
        )

        layout, pdf_path = create_comic(
            payload
        )

        return templates.TemplateResponse(

            request=request,

            name="comic_preview.html",

            context={

                "layout": layout,

                "pdf_path": pdf_path,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "error": str(exc)
            },

            status_code=500,
        )


# ====================================
# JSON API
# ====================================

@router.post(
    "/generate-comic/json"
)
async def generate_comic_json(

    payload: PromptRequest
):

    try:

        layout, pdf_path = create_comic(
            payload
        )

        return JSONResponse({

            "success": True,

            "panels": layout,

            "pdf_path": pdf_path,
        })

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)
        )


# ====================================
# EXPORT SUCCESS
# ====================================

@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(

    request: Request,

    pdf: str = "",
):

    return templates.TemplateResponse(

        request=request,

        name="export_success.html",

        context={
            "pdf_path": pdf
        },
    )


# ====================================
# IMAGE TEST ROUTE
# ====================================

@router.get(
    "/test-image"
)
async def test_image(

    prompt: str =
        "A brave fox exploring an enchanted forest"
):

    try:

        image_path = (
            generate_image_from_prompt(
                prompt
            )
        )

        return {

            "success": True,

            "image_path":
                image_path,
        }

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)
        )