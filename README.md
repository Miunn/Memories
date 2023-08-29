# Memories 

## An hosting website for *films* and *pics*

### Requirements

* Flask `^2.2.2`

### Data structure

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

### Work in progress

* Page transitions
* Admin page for uploading