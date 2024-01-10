<p align="center"><img image-rendering="pixelated" height="128px" width="128px" src="graphics/MCWebGUI-Builder_Logo.png">
<h1 align="center">MCWebGUI Builder</h1>
<p align="center"><img image-rendering="pixelated" height="256px" width="520px" src="graphics/Steve_House.png"></img></p>
<p align="center"><strong>The build tool for adding new content to MCWebGUI.</strong></p>

MCWebGUI's images have to be arranged in a very specific way, and it is just painful to add new content to it. So we made this tool to easily compile readable images into their necessary formats, this will also compile a lot of other stuff in the future, such as CSS and JavaScript files. It allows for new content to be added easily using XML configuration files.

<h1 align="center"><img image-rendering="pixelated" height="24px" width="24px" src="graphics/Installation.png">Installation</h1>

1. Download the `.exe` file, that is attached to the latest release.
2. Put it anywhere you'd like, optimally, in it's own, seperate folder.
3. Create the folders `dist` and `source` in the same folder as the `.exe`.
4. Download the `source.zip` archive from the latest release.
5. Extract included files in the archive to the `source` folder.
6. **You're done, the setup process is complete.**

<h1 align="center"><img image-rendering="pixelated" height="24px" width="24px" src="graphics/How_to_use.png">How to use</h1>
Before using MCWebGUI Builder - We  heavily recommend reading the entire README file, so you know what you're doing.

<br>

**Building Assets**
1. Run the `.exe` file in order to build the assets.
2. Navigate to the `dist` folder
3. Transfer the build assets to MCWebGUI's assets folder *as is*.
4. Start your MCWebGUI project and see if everything is working correctly.
5. **You're done, optionally, referr to Problem solving.**

**Adding new assets**

To start off, depending on wether or not you're modifying something or adding new assets, everything is configured through XML files. Subfolders are created after the name of the XML file they originate from, meaning, if you have a file called `placeholder.xml`, a new folder called "placeholder" will be created. If it is not used, it will get deleted. Preferrably, have all files from the XML file in that folder. You need to specifiy the folder in the `<result-file>` tags, but you don't have to worry about that for now.

You'll need to have the structure set up before you can do anything, so let's start with that. Create a new `.xml` file in the `source` folder. Open it in your text editor of choice, then paste the following into that file:
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

</build>
```
This structure needs to be present in *every* `.xml` file, or it will be counted as invalid. Now let's talk about the build options that are available to us:

- `rearrange` - Rearrange parts of images into three seperate repeat-files.
- `make-apng` - Create an animated PNG file from a spritesheet.
- `split` - Split a spritesheet into multiple files.
- `rescale` - Change the scale of an image.

Let's start off with `rearrange`. The structure for rearranging images goes as follows:
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Rearrange Example -->
<rearrange>
    <file></file>
    <non-repeating>
        <size></size>
        <move>
        </move>
    </non-repeating>
    <vertically-repeating>
        <size></size>
        <move>
        </move>
    </vertically-repeating>
    <horizontally-repeating>
        <size></size>
        <move>
        </move>
    </horizontally-repeating>
    <result-file></result-file>
</rearrange>

</build>
```
Woah, that's a lot. Don't worry, it's simple to understand. `<file>` is the file of the image to rearrange parts from, aka. the base image. Let's start with using the file included by default, `grid_template.png` (Make sure to include the file extension). The different `<non-repeating>`, `<vertically-repeating>` and `<horizontally-repeating>` tags are all completely optional. They are describing where the file gets saved to.

Finally, we have `<result-file>`. Let's save the rearranged images to `example/template` (Without file extension). By now, your `example.xml` file should look something like this:
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Rearrange Example -->
<rearrange>
    <file>grid_template.xml</file>
    <non-repeating>
        <size></size>
        <move>
        </move>
    </non-repeating>
    <vertically-repeating>
        <size></size>
        <move>
        </move>
    </vertically-repeating>
    <horizontally-repeating>
        <size></size>
        <move>
        </move>
    </horizontally-repeating>
    <result-file>example/template</result-file>
</rearrange>

</build>
```
Now hold tight, this might be a little bit complicated. We use a custom syntax for rearranging the images. Each single rearrangement is split by a `|` character. The rearrangement is split into two  parts by a `:`. The old position part, containing x and y position, and the size of the part to rearrange. The other part is justs the x and y coordinates on where to put it on the new image. The formatting goes a little like this:
```
0,0;4,4:0,0|
4,4;4,4:4,4
```
The semicolon splits x & y and the part size. The `<size>` tag is the size of the new image, so please make sure you have the size specified (The size is split by a comma)!

Now lets put this into action:
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Rearrange Example -->
<rearrange>
    <file>grid_template.xml</file>
    <non-repeating>
        <size>8,12</size> <!-- x,y -->
        <move>
            0,0;4,4:0,0| <!-- Top Left Corner -->
            8,0;4,4:4,0| <!-- Top Right Corner -->
            0,8;4,4:0,4| <!-- Bottom Left Corner -->
            8,8;4,4:4,4| <!-- Bottom Right Corner -->

            4,4;4,4:0,8 <!-- Center Part -->
        </move>
    </non-repeating>
    <vertically-repeating>
        <size>8,4</size> <!-- x,y -->
        <move>
            0,4;4,4:0,0| <!-- Left Edge -->
            8,4;4,4:4,0 <!-- Right Edge -->
        </move>
    </vertically-repeating>
    <horizontally-repeating>
        <size>4,8</size> <!-- x,y -->
        <move>
            4,0;4,4:0,0| <!-- Top Edge -->
            4,8;4,4:0,4 <!-- Bottom Edge -->
        </move>
    </horizontally-repeating>
    <result-file>example/grid</result-file>
</rearrange>

</build>
```

---

Now let's cover making animated PNG files. Luckily for us, this is much simpler than rearranging. First, we'll take a look at the file structure:
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Animation Example -->
<rearrange>
    <file></file>
    <size></size>
    <frame-time></frame-time>
    <loop></loop>
    <result-file></result-file>
</rearrange>

</build>
```
Let's quickly go over the tags. `<file>`, as before, is the base file to create the animation from. `<size>` is the size  of each frame, split by a comma again. `<frame-time>` is how long a frame stays. `<loop>` is the loop amount, if set to 0 it loops infinitely, if set to `none` it will not loop, aka. only play once. `<result-file>` is where the file gets put, just like before. Here's an example, with an animation included by default:
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Animation Example -->
<rearrange>
    <file>animation_template.png</file>
    <size>8,8</size>
    <frame-time>64</frame-time>
    <loop>0</loop>
    <result-file>example/animatiom</result-file>
</rearrange>

</build>
```

---

Simple right? Just as simple as splitting images:
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Split Example -->
<rearrange>
    <file></file>
    <size></size>
    <files></files>
</rearrange>

</build>
```
It's basically the same, `<file>` is the base, `<size>` is the part size and `<files>` are the names of the different files to be split (Split by a comma!).  Let's fill the information in:
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Split Example -->
<rearrange>
    <file>split_template.png</file>
    <size>32,32</size>
    <files>
        example/creeper,
        example/enderman,
        example/pig,
        example/sheep
    </files>
</rearrange>

</build>
```

---

And last but not least, the simplest one of them all. `<rescale>`! This allows you to resize the image to any dimension you want.
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Rescale Example -->
<rescale>
    <file></file>
    <size></size>
    <result-file></result-file>
</rescale>

</build>
```
This is pretty much self-explanatory by now. Let's fill the information in. 
```xml
example.xml

<?xml version="1.0" encoding="UTF-8"?>
<build>

<!-- Rescale Example -->
<rescale>
    <file>missing.png</file>
    <size>64,64</size>
    <result-file>example/rescale</result-file>
</rescale>

</build>
```

---

That's all the things you can build right now, more will be added in the future as we need it.

<p align="center"><strong>Need a little bit of help?</strong></p>
<p align="center"><strong><a href="https://discord.gg/KvZJGqMEhU"><img image-rendering="pixelated" height="64px" width="64px" src="graphics/Discord.png"><br></img>Join our Discord Server</a></strong></p>

<h1 align="center"><img image-rendering="pixelated" height="24px" width="24px" src="graphics/Problem_Solving.png">Problem solving</h1>

> **WRN** - Please create a `dist` folder before running this program.

This warning ocurrs because there is no dist folder. Please create one to solve the issue, or check if you have mispelled it.

---

> **WRN** - The `dist` folder has some files in it. Please clear it first.

The dist folder has files in it that prevent the build process from starting. You have two options:

1. You  delete the files in the `dist` folder manually
2. You can download the `clear_dist.bat` file from the latest release, to do the clearing process automatically in the future.

---

> **ERR** - The `source` folder doesn't seem to exist. Cannot continue.

This message ocurrs, because the program couldn't find a source folder to build the assets from. Check if you've mispelled the name, or if it's there in the first place.

---

> **ERR** - No `.xml` files were found in the `source` folder!

There are no `.xml` configuration files for building the assets, therefore the program cannot do anything. Check if you've got the file extension right, or if the assets from the latest release are there.

---

> **ERR** - This XML file is invalid, it cannot be processed.

Something's wrong with your `.xml` file. There could be a lot of reasons why this ocurrs, here are a few:

1. The file is empty, therefore there is nothing to be parsed.
2. You forgot the `<build>` tag, check if it's missing.
3. There's a syntax error. Check if your file structure is valid.

Are none of these the issue? Ask in [our Discord server](https://discord.gg/KvZJGqMEhU).

---

> **NIL** - No `*` parts were found.

This warning ocurrs while running a rearrange built action. It is because there are no `non-repeating`, `vertically-repeating` or `horizontally-repeating` parts. This can also ocurr when something about your `.xml` file is wrong, maybe an invalid path or one splitter (`|`) less or more.

---

> **ERR** - There seems to be some information missing. Cannot continue.

This error can ocurr while **Making an APNG file**, **Splitting Images** or **Rescaling Images**. There can be multiple reasons why this error ocurrs.

1. Tags inside the specified action have invalid content or are missing.
2. Numbers aren't valid. Check if they're correct.
3. The image is corrupted or not the right scale.

Are none of these the issue? Ask in [our Discord server](https://discord.gg/KvZJGqMEhU).

---

<p align="center"><strong>Are none of these solutions working?</strong></p>
<p align="center"><strong><a href="https://discord.gg/KvZJGqMEhU"><img image-rendering="pixelated" height="64px" width="64px" src="graphics/Discord.png"><br></img>Join our Discord Server</a></strong></p>
