# Memories 

An hosting website for *films* and *pics*

## Description

Web application to browse hosted pics and films

## Requirements

* Flask `^2.2.2`

## Data structure

Hosted pics and films must follow the next structure tree

```
|- static
    |- assets
        |- <hosted project name>
            |- img
            |    |- <imgname.*>
            |    |- ...
            |    |- <imgname.*>
            |- film
            |    |- <film.*>
            |    |- ...
            |    |- <film.*>
            |- thumbnails       # Pics and films' thumb (in picture format)    
            |    |- film
            |    |    |- <thumb.*>
            |    |    |- ...
            |    |    |- <thumb.*>
            |- <cover.*>        # Pic to display in home page
```

## The *data.json* file

The *data.json* file should contain all the data relevant to every hosted project. Each item in the json represent an hosted project. The *data.json* file saved inside the *static/* folder should follow the following structure:

```
{
    "projectname": {
        "title": str,
        "description": str,
        "headline": str,
        "subtitle": str,
        "descriptions": {
            "picname.*": str,
            ...,
            "picname.*": str
        }
    }
}
```

The descriptions field should contain the description associated with each picture. A blank string can be leave as description if there is nothing to tell. Keys are the pictures' files names with the extension.

## Work in progress

* Page transitions
* Admin page for uploading