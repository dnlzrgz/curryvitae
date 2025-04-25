# curryvitae - A Single-File CV Generator

**curryvitae** is a simple to use, single-file Python script that allows you to generate professional curriculums.

## How does it works?

curryvitae is a simple, single-file script that uses `Jinja2` as the template engine and your browser to print the final PDF file. For it to work, you will need a template, which is simply an HTML file, and a photo named `avatar.jpg` in the same directory.

> [!NOTE]
> In the `curry.html` and `spicy.html` templates included in this repository, I decided to use `Tailwind CSS` for the styles, but you can use whatever you prefer. Just remember that the important part is the printing styles.

The script is less than 250 lines of code, and I aimed to make it easy to modify and update. Therefore, if needed, it should be simple to adapt it to your needs.

## Why?

I am searching for a job, and as every good job search requires a good CV, I started looking for a tool that would allow me to build my curriculum without having to give away all my personal information. I also wanted a tool that would let me modify the template as much as I wanted and generate slightly different versions of my curriculum to better suit specific job offers. Unfortunately, I couldn't find anything that met my needs, so I decided to build my own tool.

> [!NOTE]
> If you are looking for someone to hire, feel free to check out my [portfolio](https://dnlzrgz.com) and feel free to contact me.

## Usage

Before start using it, you should:

1. Make sure that you have `uv` and `git` installed in your system.
2. Review the script before running it.
3. Add an `avatar.jpg` file to the folder in which you're going to run the script.
4. Make sure that there is at least one template file.

Once you have checked all the steps above just clone this repository:

```bash
# With gh
gh repo clone dnlzrgz/curryvitae

# Or a classic git clone
git clone https://github.com/dnlzrgz/curryvitae.git
```

Change into the `marastatic` directory:

```bash
cd marastatic
```

And finally, you can run a command like:

```bash
uv run curryvitae.py \
  --template ./spicy.html \
  --title "cv-jane-doe" \
  --full-name "Jane Doe" \
  --job-title "Web Designer" \
  --location "Berlin, Germany" \
  --summary "Creative Web Designer with over 4 years of experience in designing user-friendly websites and applications. Proficient in HTML, CSS, and JavaScript, with a strong focus on responsive design and user experience." \
  --experience "Web Designer" "2022" "" "Freelance" "Designed and developed custom websites for various clients, focusing on user experience and responsive design." \
  --experience "Junior Web Designer" "2020" "2022" "Creative Agency" "Assisted in the design and implementation of web projects, collaborating with developers and clients to meet project goals." \
  --experience "Intern Web Designer" "2019" "2020" "Design Studio" "Gained hands-on experience in web design, working on layout design and graphic elements under the guidance of senior designers." \
  --education "Graphic Design" "2020" "" "University of Arts" "" \
  --skill "HTML" \
  --skill "CSS" \
  --skill "JavaScript" \
  --skill "Adobe Photoshop" \
  --skill "Adobe Illustrator" \
  --skill "Figma" \
  --skill "Responsive Design" \
  --skill "UI/UX Design" \
  --skill "Wireframing" \
  --skill "Prototyping" \
  --skill "SEO Basics" \
  --language "German, native" \
  --language "English, fluent" \
  --language "Spanish, basic" \
  --phone-number "+4915123456789" \
  --contact-email "jane.doe@example.com" \
  --link "Portfolio" "https://janedoeportfolio.com/"
```

> [!WARNING]
> Please note that after running the script, a new Chrome window will open with a print dialog. You don't need to do anything—just be aware of it!

To learn more about each argument does you can also run:

```bash
uv run curryvitae.py --help
```

> [!TIP]
> You can check the example that's included in the repository (the PDF file) to see how the `spicy.html` template looks like. The photo used, which is also included in the repository for the example, is from [unsplash](https://unsplash.com/photos/a-man-with-a-beard-and-a-white-shirt-b7P2CrRhYf0).
