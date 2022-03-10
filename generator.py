

from typing import List, TypeVar, Optional, Tuple
import textwrap as tw
import abc


T = TypeVar('T', bound='IContent')

INDENT = '    '
ROOT = "./course_contents/"
SECTION_OPEN = "\n<section>\n"
SECTION_CLOSE = "\n</section>\n"
HTML_OPEN = """<!doctype html>
<html>"""
HTML_CLOSE = "</html>"
HEAD = """\n<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

    <title>Python Course</title>

    <link rel="stylesheet" href="dist/reset.css">
    <link rel="stylesheet" href="dist/reveal.css">
    <link rel="stylesheet" href="dist/theme/black.css">

    <style>
        body {
            cursor: url(media/cursor.png), auto;
        }
        a {
            font-size: 15px;
            margin: auto 0 0 auto;
        }
        li {
            font-size: 20px;
            margin-bottom: 20px;
        }
        .container {
            display: flex;
        }
        .col {
            flex: 1;
        }

        .column-list {
            columns: 100px;
        }
    </style>

    <!-- Theme used for syntax highlighted code -->
    <link rel="stylesheet" href="plugin/highlight/monokai.css">
</head>\n"""
BODY_OPEN = """\n<body>
    <div class="reveal">
        <div class="slides">\n"""
BODY_CLOSE = """\n</div>
	</div>
    <script src="dist/reveal.js"></script>
    <script src="plugin/notes/notes.js"></script>
    <script src="plugin/markdown/markdown.js"></script>
    <script src="plugin/highlight/highlight.js"></script>
    <script>
        // More info about initialization & config:
        // - https://revealjs.com/initialization/
        // - https://revealjs.com/config/
        Reveal.initialize({
            hash: true,
            parallaxBackgroundImage: 'https://background-tiles.com/overview/black/patterns/large/1035.png',
            parallaxBackgroundSize: '300px 300px',
            parallaxBackgroundHorizontal: 200,
            parallaxBackgroundVertical: 50,

            // Learn about plugins: https://revealjs.com/plugins/
            plugins: [ RevealMarkdown, RevealHighlight, RevealNotes ]
        });
    </script>
</body>\n"""

def read_file(path: str) -> str:
    f = open(path, "r")
    c = f.read()
    f.close()
    return c

def write_file(path: str, content: str) -> None:
    f = open(path, "w")
    f.write(content)
    f.close()

class IContent( metaclass=abc.ABCMeta ):

    @property
    def path(self) -> str:
        return self._path

    def build(self, path: str):
        return "".join(map(lambda x : tw.indent(x, INDENT), [
            SECTION_OPEN,
            self.contents(path),
            SECTION_CLOSE
        ]))

class HtmlSegment( IContent ):
    """Represents HTML snippet. Part of composite design pattern for revealJS.

    Finds the .html file in question and inserts it into the final target 
    document with the help of the composite design pattern.

    USE:
        >>> HtmlSegment(rel_path + 'filename.html')

    IMPORTANT:
        Do not include the <section> tags in the .html file - they will be 
        wrapped around this element at compile-time.
    """
    
    def __init__(self, path: str):
        super().__init__()
        self._path = path

    def contents(self, ch_path) -> str:
        return self.format_html(read_file(ch_path + self.path))
    
    def format_html(self, content: str) -> str:
        return tw.indent(content, INDENT)

class CodeSegment( IContent ):
    """Represents Python code snippet. Part of composite design pattern.

    Finds the .py file in the contents containing the target Python code to be
    displayed in the course. Title is provided to be put on top of the code, 
    for information. The rule corresponds to the optional value that can be 
    provided - it is used by the revealJS interpreter. 

    USE:
        >>> CodeSegment(rel_path + 'listc.py', "List Comprehension", '1,2|3-4')

    IMPORTANT:
        In the .py snippet file, please LEAVE THE FIRST LINE EMPTY.
    """

    def __init__(self, path: str, title: str, rule: Optional[str] = None):
        super().__init__()
        self._path = path
        self._rule = rule
        self._title = title

    @property
    def rule(self) -> str:
        return self._rule if self._rule else ''

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def language(self) -> str:
        if self.path.split('.')[-1] == 'py':
            return 'python'
        elif self.path.split('.')[-1] == 'html':
            return 'html'
    
    def contents(self, ch_path: str):
        return "\n".join([
            self.format_title(), 
            self.format_code(read_file(ch_path + self.path))
        ]) 

    def format_title(self) -> str:
        return f"<h3>{self.title}</h3>"

    def format_code(self, code: str) -> str:
        code = code\
            .replace('&', '&amp;')\
            .replace('<', '&lt;')\
            .replace('>', '&gt;')

        return f"""<pre><code class='language-{self.language}' \
            data-trim data-noescape \
            data-line-numbers='{self.rule}'>
        
        {tw.indent(code, INDENT)}
        
        </code></pre>"""

class ContainingSegment( IContent ):
    """Node element in the composite design pattern.

    Basic element of the composite design pattern used for this project. The 
    classes implementing the IContent interface can be held using this class.

    USE:
        >>> tree = ContainingSegment(
        ...     IContent-subclass,
        ...     IContent-subclass,
        ...     IContent-subclass,
        ...     chapter_path="./path_to_chapter/"
        ... )
        >>> output_string = tree.compile()
    """

    def __init__(self, *args: T, chapter_path: str = ""):
        super().__init__()
        self._children = args
        self._path = ROOT + chapter_path

    @property
    def children(self) -> Tuple[T, ...]:
        return self._children

    def contents(self, ch_path: str) -> str:
        return "\n".join([c.build(self.path) for c in self.children])

    def compile(self) -> str:
        return HTML_OPEN + "".join(map(lambda x : tw.indent(x, INDENT), [
            HEAD,
            BODY_OPEN,
            "\n".join([
                c.build(self.path) for c in self.children
            ]),
            BODY_CLOSE
        ])) + HTML_CLOSE

if __name__ == '__main__':
    root = "./course_contents/"
    index_path = './index.html'

    flask_1 = ContainingSegment(
        HtmlSegment("landing.html"),
        HtmlSegment("descriptionflask.html"),
        HtmlSegment("whouses.html"),
        CodeSegment("setup.py", "La mise en place", "1-6|8-15"),
        CodeSegment("routes.py", "Les routes", "4-7|9-15|17-20|22-25|27-30"),
        CodeSegment("request_object.py", "L'objet requête", "1-3|7-17"),
        CodeSegment("responses.py", "Les réponses", "6-17|19-29|31-38|40-41"),
        HtmlSegment("exercise.html"),
        CodeSegment("error_handling.py", "La gestion des erreurs", "4-16"),

        chapter_path="flask_1/"
    )

    flask_2 = ContainingSegment(
        HtmlSegment("layout.html"),
        CodeSegment("factory.py", "La fabrique de l'app", "1-7|9-22"),
        CodeSegment("blueprint.py", "Le blueprint", "1-11|14-20"),
        HtmlSegment("mini-exercise.html"),
        CodeSegment("database.py", "La base de données", "1-5|8-16|19-23|27-44|48-57|60-65|68-70|74-80"),
        CodeSegment("base.html", "Le gabarit HTML de base", "1|3-12|18-24|25-32|37-45"),
        CodeSegment("register.html", "Le formulaire d'enregistrement", "3|5-7|9-19"),
        CodeSegment("login.html", "Le formulaire de login", "3|5-7|9-19"),

        chapter_path="flask_2/"
    )

    flask_3 = ContainingSegment(
        CodeSegment("auth.py", "L'authentification", "1-6|9-14|17-22|24-26|28-36|38-52|54-56|58-62|64-65|67-71|74-79|81-83|85-90|92-100|102-111|113-114|116-120|123-127|129-131|133-138|141-147|150-153|155-157|159-164|166-168|170-171|173-177|181-186"),
        HtmlSegment("mini-exercise.html"),
        CodeSegment("database.py", "La base de données II", "1-6|10-20|22-26|29-35|37-39|41-47|49-57|59-62|64-65|67-71|74-85|87-97|99-100|103-113|115-117|119-125|127-134|136-139|141-142|144-149|152-162|164-167"),
        CodeSegment("index.html", "La liste des articles", "1-2|4-12|14-16|18-24|25-33|36|39-43"),
        CodeSegment("create.html", "Le form de création", "1-2|4-6|8-9|10-14|16-20|22|23-24"),
        CodeSegment("edit.html", "La form de édition", "1-2|4-8|10-11|12-18|20-27|29|34-38|40-41|42-43"),
        HtmlSegment("mini-exercise-2.html"),
    
        chapter_path="flask_3/"
    )

    flask_4 = ContainingSegment(
        HtmlSegment("landing.html"),

        CodeSegment("jwt.py", "Les JSON Web Tokens", "1|5-17|21-27|30-35|38-40|42-45|47-52|54-65|67-75|77-82|85-89|90-95|97-105"),
        HtmlSegment("mini-exercise.html"),
        CodeSegment("env.py", "Le fichier .env", "1|5-9|13-16|18-27"),
        CodeSegment("install.py", "Rendre l'app installable", "1|5|8-19|23-29|33-37"),
        
        chapter_path="flask_4/"
    )

    '''
    flask_5 = ContainingSegment(
        CodeSegment("emails.py", "Les emails de confirmation", "1|5-14|18-20|22-25|27-33|35-36|40-47|51-53|56-58|60-63|65-69|72-74|76-79|81-87|89-91|93-94|98-99|102-106|108-109|111-115|117-122|124-128|130-137|139-142|144-147|150-155|157-160|162-167|169-173|175-176|178-179|181-186"),
        CodeSegment("sql_alchemy.py", "Le ORM SQLAlchemy", "1|5-13|16-17|20-33|37-44|47-55|58-65|67-76|78-86|88-96|98-107"),
        HtmlSegment("the_end.html"),

        chapter_path="flask_5/"
    )
    '''

    template = ContainingSegment(
        flask_1,
        flask_2,
        flask_3,
        flask_4,
        #flask_5
    )

    write_file(index_path, template.compile())

    print(template.compile())

