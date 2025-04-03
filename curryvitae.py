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
# Command
# ==============================


@click.command()
@click.option(
    "--template",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to the template file to be used for generating the CV.",
)
@click.option(
    "--title",
    type=str,
    help="Title of the document (e.g., 'cv-john-doe').",
)
@click.option(
    "--full-name",
    "--name",
    type=str,
    help="Your full name as you want it to appear on the CV.",
)
@click.option(
    "--job-title",
    "--position",
    type=str,
    help="Your current job title or position.",
)
@click.option(
    "--location",
    type=str,
    help="Your current location (e.g., 'city, country').",
)
@click.option(
    "--summary",
    "--description",
    type=str,
    help="Summary or description of your professional background.",
)
@click.option(
    "--experience",
    "--exp",
    type=(str, str, str, str),
    multiple=True,
    help="Work experience in the format: Company, start date, end date, description.",
)
@click.option(
    "--education",
    "--edu",
    type=(str, str, str, str),
    multiple=True,
    help="Education in the format: Grade and institution, start date, end date, description.",
)
@click.option(
    "--skill",
    type=str,
    multiple=True,
    help="List of relevant skills.",
)
@click.option(
    "--language",
    "--lang",
    type=(str, str),
    multiple=True,
    help="Languages you speak along with your preficiency level (e.g., 'Spanish' 'Native').",
)
@click.option(
    "--phone-number",
    "--phone",
    type=str,
    help="Your phone number.",
)
@click.option(
    "--contact-email",
    "--email",
    type=str,
    help="Your contact email.",
)
@click.option(
    "--link",
    "--url",
    type=(str, str),
    multiple=True,
    help="Links to your online profiles or social networks in the format: 'URL', 'link name'.",
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
                title=exp[0],
                start_date=exp[1],
                end_date=None if exp[2] == "" else exp[2],
                description=exp[3],
            )
            for exp in experience
        ],
        education=[
            TimelineEvent(
                title=edu[0],
                start_date=edu[1],
                end_date=None if edu[2] == "" else edu[2],
                description=edu[3],
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

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--kiosk-printing")

        driver = webdriver.Chrome(options=chrome_options)

        print_options = PrintOptions()
        print_options.orientation = "portrait"
        print_options.page_height = 27.94  # A4's height
        print_options.page_width = 21.59  # A4's width'

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
