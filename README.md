# CurryVitae

A single-file script for generating your curriculum.

## What is this?

CurryVitae is a simple Python script that makes easier the process of generating your curriculum by using `Jinja2` for the templating and a web browser for rendering and printing the final PDF file.

With less than 250 lines of code, the script is easy to understand and modify, allowing you to customize it to better suit your needs if necessary.

## Why?

I'm in search of a job and wanted a tool that would allow me to create a customizable curriculum, easy to adapt and modify for each job position, without having to sell all my personal information in order to use it. The result is a simple script that enables me to generate my resume in less than 5 seconds, with an input format that is easy to use and can even be combined with AI to enhance it if wanted.

## How does it works?

The script works in 3 main steps:

1. It receives your details through a series of command-line arguments, including your full name, job title, location, summary, and more.
2. Then the specified HTML template is retrieved and `Jinja2` is used to render a temporary HTML file with the result.
3. Finally, `selenium` is used to launch a Chrome instance that opens the temporary file and prints out a PDF.

> [!NOTE]
> The temporary HTML file is removed at the end, and the resulting PDF file is saved using the title specified via the corresponding command-line argument.

## Usage

Before start using it, you should:

1. Ensure that you have `uv` installed in your system.
2. Check the script before running it.
3. Add an `avatar.jpg` file to the folder in which you're going to run the script.

Now, after all this is done, you can run something like:

```bash
uv run curryvitae.py \
  --template ./curry.html \
  --title "cv-emma-johnson" \
  --full-name "Emma Johnson" \
  --job-title "Graphic Designer" \
  --location "Berlin, Germany" \
  --summary "I am a passionate Graphic Designer with over 6 years of experience in creating visually compelling designs for both print and digital media. My expertise includes branding, typography, and user interface design, with a strong focus on user experience." \
  --experience "Senior Graphic Designer" "2021-02-01" "2023-10-01" "Led a team of designers to create branding and marketing materials for various clients." \
  --experience "Graphic Designer" "2018-01-01" "2021-01-31" "Designed promotional materials, including brochures, posters, and social media graphics." \
  --experience "Junior Graphic Designer" "2016-06-01" "2017-12-31" "Assisted in the design of web and print materials, collaborating with senior designers." \
  --education "Bachelor of Arts in Graphic Design @ University of Arts" "2012-09-01" "2016-05-15" "Graduated with distinction." \
  --skill "Adobe Photoshop" \
  --skill "Adobe Illustrator" \
  --skill "Adobe InDesign" \
  --skill "Figma" \
  --skill "Sketch" \
  --skill "HTML/CSS" \
  --skill "Branding" \
  --skill "UI/UX Design" \
  --skill "Typography" \
  --skill "Color Theory" \
  --language "English" "Native" \
  --language "German" "Fluent" \
  --language "Spanish" "Intermediate" \
  --phone-number "+4915123456789" \
  --contact-email "emma.johnson@example.com" \
  --link "Portfolio" "https://emmajohnsondesigns.com/"
```

To learn more about each argument does you can also run:

```bash
uv run curryvitae.py --help
```

> [!TIP]
> The `curry.html` file provides an example template that uses Tailwind CSS for styling, but you can use any styling framework or custom styles you prefer. The key point to remember is that the appearance of the page in the browser is not what matters; what’s important is how it looks in the print dialog and the final PDF file.
