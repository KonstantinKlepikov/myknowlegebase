---
description: Шаблонизирование документации python проекта в sphynx
title: sphynx templates
tags: templating python
---
Sphynx - генератор документации для python проектов.

## [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)

- one asterisk: \*text\* for emphasis (italics),
- two asterisks: \*\*text\*\* for strong emphasis (boldface),
- backquotes: \`\`text\`\` for code samples.

### Lists and Quote-like blocks

```shell
* This is a bulleted list.
* It has two items, the second
  item uses two lines.

1. This is a numbered list.
2. It has two items too.

#. This is a numbered list.
#. It has two items too.
```

```shell
* this is
* a list

  * with a nested list
  * and some subitems

* and here the parent list continues

term (up to a line of text)
   Definition of the term, which must be indented

   and can even consist of multiple paragraphs

next term
   Description.
```

```shell
| These lines are
| broken exactly like in
| the source file.
```

### Literal code blocks

```shell
This is a normal text paragraph. The next paragraph is a code sample::

   It is not processed in any way, except
   that the indentation is removed.

   It can span multiple lines.

This is a normal text paragraph again.
```

### Doctest blocks

```shell
>>> 1 + 1
2
```

Tables

```shell
+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | ...        | ...      |          |
+------------------------+------------+----------+----------+
```

or

```shell
=====  =====  =======
A      B      A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======
```

### Hyperlinks

```shell
`Link text <https://domain.invalid/>`
```

or

```shell
This is a paragraph that contains `a link`_.

.. _a link: https://domain.invalid/
```

### Sections

- \# with overline, for parts
- \* with overline, for chapters
- = for sections
- \- for subsections
- ^ for subsubsections
- " for paragraphs

```shell
=================
This is a heading
=================
```

### Field Lists

Списки полей представляют собой последовательности полей, размеченных следующим образом: `:fieldname: Field content`

```shell
def my_function(my_arg, my_other_arg):
    """A function just for me.

    :param my_arg: The first of my arguments.
    :param my_other_arg: The second of my arguments.

    :returns: A message (just for me, of course).
    """
```

[Подробнее](https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html)

### [Roles](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html)

Роль или «пользовательская интерпретируемая текстовая роль» — это встроенный фрагмент явной разметки. Это означает, что вложенный текст следует интерпретировать определенным образом. Sphinx использует это для обеспечения семантической разметки и перекрестных ссылок идентификаторов. Общий синтаксис: :rolename:`content`. Поддерживаются, к примеру:

- emphasis – equivalent of \*emphasis\*
- strong – equivalent of \*\*strong\*\*
- literal – equivalent of \`\`literal\`\`
- subscript – subscript text
- superscript – superscript text
- title-reference – for titles of books, periodicals, and other materials

Пример: Since Pythagoras, we know that :math:`a^2 + b^2 = c^2`.

### Explicit Markup

«Явная разметка» используется в reST для большинства конструкций, требующих специальной обработки, таких как сноски, специально выделенные абзацы, комментарии и общие директивы.

Блок явной разметки начинается со строки, начинающейся с `..`, за которой следует пробел, и заканчивается следующим абзацем с тем же уровнем отступа. (Между явной разметкой и обычными абзацами должна быть пустая строка.

### [Dicrectives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html)

Директива — это общий блок явной разметки. Наряду с ролями это один из механизмов расширения reST.

[Подробнее тут](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#directives)

### Others

Изображения, сноски, комментарии - [смотри ниже](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#images)

Подробнее обо всем этом тут: [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)

## [Markdown](https://www.sphinx-doc.org/en/master/usage/markdown.html)

## [Configuration](https://www.sphinx-doc.org/en/master/usage/configuration.html)

## [Extentions](https://www.sphinx-doc.org/en/master/usage/extensions/index.html)

- sphinx.ext.autodoc – Include documentation from docstrings
- sphinx.ext.autosectionlabel – Allow reference sections using its title
- sphinx.ext.autosummary – Generate autodoc summaries
- sphinx-autogen – generate autodoc stub pages
- sphinx.ext.coverage – Collect doc coverage stats
- sphinx.ext.doctest – Test snippets in the documentation
- sphinx.ext.duration – Measure durations of Sphinx processing
- sphinx.ext.extlinks – Markup to shorten external links
- sphinx.ext.githubpages – Publish HTML docs in GitHub Pages
- sphinx.ext.graphviz – Add Graphviz graphs
- sphinx.ext.ifconfig – Include content based on configuration
- sphinx.ext.imgconverter – A reference image converter using Imagemagick
- sphinx.ext.inheritance_diagram – Include inheritance diagrams
- sphinx.ext.intersphinx – Link to other projects’ documentation
- sphinx.ext.linkcode – Add external links to source code
- sphinx.ext.imgmath – Render math as images
- sphinx.ext.mathjax – Render math via JavaScript
- sphinx.ext.jsmath – Render math via JavaScript
- sphinx.ext.napoleon – Support for NumPy and Google style docstrings
- sphinx.ext.todo – Support for todo items
- sphinx.ext.viewcode – Add links to highlighted source code

## [[setuptools]] integrations

[link](https://www.sphinx-doc.org/en/master/usage/advanced/setuptools.html)

## [Extending](https://www.sphinx-doc.org/en/master/development/index.html)

Смотри еще:

- [Using Sphinx](https://www.sphinx-doc.org/en/master/usage/index.html)
- [reStructuredText Primer docs](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [reStructuredText Markup Specification](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#paragraphs)
- [sphynx themes galery](https://sphinx-themes.org/#themes)
- [Napoleon - Marching toward legible docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html)
- [How do I create a new line with reStructuredText](https://stackoverflow.com/questions/51198270/how-do-i-create-a-new-line-with-restructuredtext)
- [[шаблонизаторы]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[setuptools]: setuptools "Setuptools"
[шаблонизаторы]: ..%2Flists%2F%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80%D1%8B "Шаблонизаторы"
[//end]: # "Autogenerated link references"