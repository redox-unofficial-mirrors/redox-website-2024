# Redox-OS Website

The source for the Redox-OS Website can be found at this repository. It's structure and function, as well as its maintenance is outlined below. 

## How it works

The website is designed to run on GitHub Pages. This means that the site, regardless of the complexity of its source must compile to a static website, which can be hosted by a fileserver. This leaves a few difficult-to-tackle challenges. Such as the inclusion of more complex document types used for curating content. 

A core feature is the ability to edit web content using Microsoft Word. Unfortunately, this requirement isn't met by GitHub Pages' standard build-system, Jekyll. Thus, the website's source must be compiled manually. This is the role of the python files scattered throughout the sourcetree. 

Notably the root of the source tree contains sevaral important files which allow the website's source to be compiled into a final bundle of pages and assets.

### Scripts

| Script | Function |
|---|---|
| `build.py` | This is the entrypoint to the build system. It compiles and bundles everything into a final packageable bundle which can be deployed to GitHub Pages or any other static-filehost. By invoking this script, you are building the site from beginning to end |
| `template.py`, `template_utils.py` | These files provide the ability to wrap the content of each page into a uniform frame, allowing for semi-dynamic[^1] content. |
| `docx.py`, `md.py`, `html.py` | These represesent the various supported filetypes which the build script knows how to compile. They follow a common API, and are invoked as subprocesses, allowing for parallelisation, and graceful failure-handling |
| `redirect.py` | This file represents the filetype for all symbolic links. It maps the link to its destination and returns a page which contains a client-side redirect. |
| `template.html` | Contains the skeleton of each returned page. It includes other template-resources, such as `head.html`, (The contents of the `<head>` tag), or the `frame.html` (whose job is to display each templated page in a friendly manner, i.e. populating the non-content areas of the page) or the `footer.html` (which contains links to various resources around the site, as well as important legal information). |

### Pages

A page is any file in any content root with an corresponding filetype handler. i.e. a file which the build script has the ability to compile into a webpage. By default, there exists only one content-root, `#/pages`. All files will be attempted to convert into webpages, but some may be of unsupported formats. These are skipped. The format is determined by its file-extension. 

Each page **must** be annotated with a language. A file without a language annotation is ignored, regardless of whether the build-script supports it. The annotation is a set of characters between dots, placed directly before the file extension. i.e. the last two dot-sections are interpreted. 

An example may be `index.en.html`. This file is indicated to be of type `html`, and written in english. 

The language extension allows the build script to find _translations_ of the file. Links to the translated versions are built in to the final page. See (`frame.html`)[./frame.html#L5] for source.

Note that there is no restriction on the contents or even existence of translations. As long as they follow the given naming scheme, translations happen automatically, and users can quite cleanly switch languages. 

## Build automation

Having the requirements to run on GitHub Pages, a recent addition is the support for compilation workflows to run on GitHub Actions. This is made-use-of in the automatic deployment to Pages. The deployment script can be found at [`.github/workflows/pages.yml`](.github/workflows/pages.yml). It covers the following steps:

### 1. Check out source-code
This step downloads the latest version of the website and ensures its availability to build scripts

### 2-4. Install Dependences
The build script depends on:
* Python
* Markdown-it-py
* Pandoc

These are installed and validates

### 5-6. Prepare build
The filesystem needs to be prepared in order to write to the correct destinations. This involves:
* Deleting old or stale build-artifacts
* Ensuring the necessary directory structure is in-placed
* Making sure the necessary scripts have executable permissions
* All the resulting artifacts follow the required naming conventions

### 7. Linking the top-level files to their language-specified equivalent. 
To make the webpage more friendly to users navigating to `/`, there should exist an `/index.html` file. Since it's possibly ambiguous which language this file may be specified in, this is left to the developer to link the at the root to the final destinations. This is done via client-side redirects for obvious reasons. 

### 8. Building artifacts
As outlined above, the build script converts the sources to the final pages via a template. This is applied in this step by invoking the `build.py` script

### 9. Bundling
GitHub Pages requires that sites be deployed in .tar.gz format. i.e. the website's contents must be archived. The bundling process ensures the necessary files are placed into the appropriate bundle format. 

### 10. Upload
By uploading the artifact, the site is scheduled for deployment, which involves behind-the-scenes processes at GitHub to expose the contents of the archive to the wider web. 

If any step during this process fails, i.e. returns a non-zero exit code, the workflow is cancelled, and the latest version of the website never reaches publication. 

## Alternative deployments

Since the website's contents are entirely static, it can be uploaded to any host which supports static file serving (which is the vast majority). Services like NGinx can even expose FTP channels by which it can be updated completely automatically. To achieve this, the build script needs to be adjusted accordingly. Any resources such as private SSH keys can be added via the repository's _secrets_ settings, ensuring no secrets ever become exposed through source-code. 

## Occasional maintenance procedures

In the future, it's possible that pages become disorganised, by things like inconsistent casing, or malformed contents. It's recommended that documents such as Word documents use predefined styles to make the various heading-levels as explicit as possible. This decreases the likelihood of false conversions by Pandoc to virtually zero. 

Occasionally, Markdown documents can be formatted to conform with standards guidelines, such as line-lengths, table syntax and consistent bold-italic annotations etc.

### Guides to good CSSing
CSS is virtually impossible to write cleanly or elegantly. Therefore to make maintaining it as straight-forward as possible, we ask maintainers to follow a few certain rules:

1. Try to reuse styles. 
    Elements tend to be classifiable into various widget-like structures. Reuse these as much as possible. 
    
    * Selectors for elements within widgets should use fully qualified selectors, relative to the topmost child of the widget. 
        This prevents styles within widgets from affecting elements outside of the widget.
        
    * Attempt to combine selectors where possible. 
        If various elements use very similar styles, it's best to factorise the common styles, and apply smaller rules to more widgets, than inversly.
        
    * Define a global theme system.
        Dimensions, fonts, colours, shadows, layouts etc should be defined in various levels using descriptive names. This allows dynamic theming to adjust generic variables with predefined contents. 
        
        An example may be a light-dark colour scheme. The theme defines two colours; a light and a dark colour, named `white` and `black` respectively. Then defines variables called `foreground` and `background`. Using media queries, the `foreground` and `background` variables can be populated with the values of predefined colours. Light might specify `background` to hold the value `white` while Dark specifies it to hold `black`.
        
        This system allows defining of colour schemes in a very modular, yet precise manner. It also allows exceptions to this rule, such as accent colours being defined at the choice of the user, or _Danger_ buttons using predefined colours, such as accent colours, which happen to be red etc. 
        
        This holds true for dimensions and fonts etc, but is most prominent with colours.
        
2. In the event that a truly custom widget needs creating, its styles should be contained in a separate CSS structure.

3. Group styles logically.
    Styles are applied in top-to-bottom order, which often leads to cluttered styles files. 
    
    * Attempt to keep the workspace clean by logically grouping these according to the order of elements defined in markup, as well as grouping styles which apply to certain widgets in correspondingly-named styles files, containing only styles for that widget. 

    * The `@import` rule gives the possibility to recreate the file structure as though all styles were entered into a file. This can be very beneficial when the order of styles should become relevant.
    
4. Don't reinvent the wheel.
    HTML offers various predefined widgets which fill common purposes, however can be famously hard to make look nice. This often leads developers to implementing their own widgets. In almost all cases, this is done imperfectly, leading to reduced user-experiences in certain edge-cases. 
    
    * When possible, attempt to restyle existing widgets, or build up the widget's functions using existing widgets.
    
    * Use styles which are already defined to further reduce the amount of styles which need to be defined and maintained.
    
5. CSS is and should remain static.
    While it's possible to change the stylesheets in a running environment, this often leads to inelegant or messy code.
    
    * If a widget's style needs to be altered dynamically, this should be implemented by managing the list of classes an element belongs to. 
    
    * In the event this is not adequate, alterations to the CSS source should be strictly limited to the theme variables discussed earlier. This ensures the style changes are not localised to a single widget. 
    
6. Don't use *Magic* to make things happen. 
    *Magic* makes a system unmaintainable, as its behaviour is not always clear. 
    
    * Attempt to factorise the necessary styles or behaviour into reusable rules or functions.
    
    * Reduce the use of JavaScript in interactivity.
    
7. For complex behaviours, using UI frameworks like React can allow the necessary complexity to be implemented without interfering with non-complex pages.

    * The build system will need to be updated to allow building SPAs.
    
    * Attempt to define a filetype for this, allowing for as much reuse as possible.

    
## Version-Control

The version-control history may be somewhat untidy due to the indented author-base. Maintainers are recomended to make large-scale changes on separate branches, such that in the event of a breaking change, content can be migrated gradually. 

### GitFS

To allow for easy curation of contents, it's possible to mount a git repository like a filesystem, making every change a separate commit. This will continue to clutter the version history. For this reason, it's recommended to deploy a development version using a private namespace of some kind. 

The following setup can be utilised to make development as straight-forward as possible. 

1. Using a VPS or Dedicated server, the source code of the website can be cloned in a development-environment. Using tools like Samba, exposed to authors. 
    Ideally, only the required page roots should be exposed, limiting the access of authors to various regions of the codebase. 
    
2. The following tools are recommended for working on contents:

    * Python 3.10+
    * Pandoc 2.1+
    * Caddy HTTP Server
    * Microsoft Word
    * Microsoft Word Markdown plugins
    * Samba
    * SSH
    * entr
    
3. The website can be hosted using Caddy's inbuilt file-server capabilites, serving the build resources.
    * Using tools like `entr`, the contents of the website can be rebuilt on file changes.

4. Deploy a management portal
    * To make publication more straight-forward, a dedicated development-only page can be exposed to authors to push the contents of the website to GitHub, where it is built, and deployed to the host. This might be achieved with a direct SSH connection to the VPS which issues commands directly from the interface, including combinations of `git commit` and `git push`, restarting services, or monitoring builds and deployments.    

5. It's possible to write a GUI webpage builder
    A long-term goal is to simplify the web-curation process as much as possible. This might include graphical webpage editors. 
    
## Deployment

The deployment process is as-of-present simply an SCP step. However due to the strict requirement for cryptographic integrity, several steps are required to keep the system running consistently. Consequently, there are four secrets registered on the Action which allow the script to push the bundled source to the corresponding destination. 

The four secrets are:

* `sshprivkey`: Contains the PAM-encoded private key SSH can use to authenticate itself with the host
* `host`: The hostname or IP of the destination server
* `user`: Host's username used to authenticate
* `destination`: Where the final build resources are copied to

These should be updated regularly, most likely with identical information. If a deploy fails, it's very likely due to a misconfiguration of any of the four values listed above. 

---

# Copyright Notice

Copyright © 2015-2024 by Redox Developers. Redox OS is a trademark of the Redox OS nonprofit.