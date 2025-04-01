# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
#     "email-validator",
#     "jinja2",
#     "phonenumbers",
#     "pydantic",
#     "pydantic-extra-types",
#     "rich",
# ]
# ///

from datetime import date
from enum import Enum
from pathlib import Path
import click
from rich import print
from pydantic import BaseModel, EmailStr, HttpUrl
from pydantic_extra_types.phone_numbers import PhoneNumber
from jinja2 import Environment
from jinja2 import FileSystemLoader

# ==============================
# Models
# ==============================


class ProficiencyLevel(str, Enum):
    ELEMENTARY = "Elementary"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    FLUENT = "Fluent"
    NATIVE = "Native"


class TimelineEvent(BaseModel):
    title: str
    start_date: date
    end_date: date | None = None
    description: str


class SocialLink(BaseModel):
    name: str
    url: HttpUrl


class Language(BaseModel):
    language: str
    proficiency: ProficiencyLevel


class Curry(BaseModel):
    full_name: str | None = None
    job_title: str | None = None
    location: str | None = None
    summary: str | None = None

    experience: list[TimelineEvent] = []
    education: list[TimelineEvent] = []
    skills: list[str] = []

    languages: list[Language] = []

    phone_number: PhoneNumber | None = None
    contact_email: EmailStr | None = None
    website: HttpUrl | None = None
    social_links: list[SocialLink] = []


# ==============================
# Templating
# ==============================
def render(curry: Curry):
    print(curry.model_dump())


# ==============================
# CLI
# ==============================


@click.command()
@click.option(
    "--template",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to the template file",
)
@click.option(
    "--full-name",
    type=str,
    help="Full name",
)
@click.option(
    "--job-title",
    type=str,
    help="Job title or position",
)
@click.option(
    "--location",
    type=str,
    help="Current location",
)
@click.option(
    "--summary",
    type=str,
    help="Summary or description",
)
@click.option(
    "--experience",
    type=(str, str, str, str),
    multiple=True,
    help="Experience",
)
@click.option(
    "--education",
    type=(str, str, str, str),
    multiple=True,
    help="Education",
)
@click.option(
    "--skill",
    type=str,
    multiple=True,
    help="Skill",
)
@click.option(
    "--language",
    type=(str, str),
    multiple=True,
    help="Languages",
)
@click.option(
    "--phone-number",
    type=str,
    help="Phone number",
)
@click.option(
    "--contact-email",
    type=str,
    help="Contact email",
)
@click.option(
    "--website",
    type=str,
    help="Personal website",
)
@click.option(
    "--link",
    type=(str, str),
    multiple=True,
    help="Social links",
)
def cli(
    template,
    full_name,
    job_title,
    location,
    summary,
    experience,
    education,
    skill,
    language,
    phone_number,
    contact_email,
    website,
    link,
):
    curry = Curry(
        full_name=full_name,
        job_title=job_title,
        location=location,
        summary=summary,
        experience=[
            TimelineEvent(
                title=exp[0], start_date=exp[1], end_date=exp[2], description=exp[3]
            )
            for exp in experience
        ],
        education=[
            TimelineEvent(
                title=edu[0], start_date=edu[1], end_date=edu[2], description=edu[3]
            )
            for edu in education
        ],
        skills=list(skill),
        languages=[
            Language(language=lang[0], proficiency=ProficiencyLevel(lang[1]))
            for lang in language
        ],
        phone_number=phone_number,
        contact_email=contact_email,
        website=website,
        social_links=[SocialLink(name=url, url=name) for (url, name) in link],
    )

    try:
        template_path = Path(template)
        env = Environment(loader=FileSystemLoader(template_path.parent))
        template_name = template_path.name

        template = env.get_template(template_name)
        rendered_output = template.render(curry=curry.model_dump())

        output_file = Path("./cv.html")
        with output_file.open("w", encoding="utf-8") as f:
            f.write(rendered_output)
    except Exception as e:
        print(f"[bold red]ERROR[/]: something went wrong: {e}")


if __name__ == "__main__":
    cli()
