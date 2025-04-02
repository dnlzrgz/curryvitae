# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click",
#     "email-validator",
#     "jinja2",
#     "phonenumbers",
#     "pydantic",
#     "pydantic-extra-types",
#     "selenium",
# ]
# ///

import base64
import os
from datetime import date
from enum import Enum
from pathlib import Path
import click
from pydantic import BaseModel, EmailStr, HttpUrl
from pydantic_extra_types.phone_numbers import PhoneNumber
from jinja2 import Environment
from jinja2 import FileSystemLoader
from selenium import webdriver
from selenium.webdriver.common.print_page_options import PrintOptions

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


class Link(BaseModel):
    name: str
    url: HttpUrl


class Language(BaseModel):
    language: str
    proficiency: ProficiencyLevel


class Curry(BaseModel):
    title: str

    full_name: str
    job_title: str
    location: str
    summary: str

    experience: list[TimelineEvent]
    education: list[TimelineEvent]
    skills: list[str]

    languages: list[Language]

    phone_number: PhoneNumber | None = None
    contact_email: EmailStr
    links: list[Link] = []


# ==============================
# Chrome setup
# ==============================
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--kiosk-printing")

driver = webdriver.Chrome(options=chrome_options)

print_options = PrintOptions()
print_options.orientation = "portrait"

print_options.page_height = 27.94  # A4's height
print_options.page_width = 21.59  # A4's width'


# ==============================
# Command
# ==============================


@click.command()
@click.option(
    "--template",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to the template file",
)
@click.option(
    "--title",
    type=str,
    help="Title of the document",
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
    "--link",
    type=(str, str),
    multiple=True,
    help="Links",
)
def cli(
    template,
    title,
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
    link,
):
    curry = Curry(
        title=title,
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
        links=[Link(name=url, url=name) for (url, name) in link],
    )

    try:
        template_path = Path(template)
        env = Environment(loader=FileSystemLoader(template_path.parent))
        template_name = template_path.name

        template = env.get_template(template_name)
        rendered_output = template.render(curry=curry.model_dump())

        temp_file = Path("./temp.html")
        with temp_file.open("w", encoding="utf-8") as f:
            f.write(rendered_output)

        driver.get(f"{temp_file.absolute().as_uri()}")

        pdf = driver.print_page(print_options)
        pdf_data = base64.b64decode(pdf)
        with open(f"{curry.title}.pdf", "wb") as f:
            f.write(pdf_data)

        os.remove(temp_file)

        driver.quit()
    except Exception as e:
        click.echo(f"ERROR: something went wrong: {e}")


if __name__ == "__main__":
    cli()
