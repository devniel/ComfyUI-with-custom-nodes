# Get Batch from History

This experimental node does something really simple, it reads the outputs from the history endpoint of Comfy.
Outputs gets populated by... output nodes. There are various ones but  for instance in core comfy, `Save Image` and `Preview Image` are output nodes.
I advice to start simple and have workflows that only generates one output per queue run. Of course once you master it you can use multiple outputs as output order is kept (as long as all outputs are ran).

Another basic use case of batch from history that you can see in the 4th [example](Examples), the fake deforum effect, basically this flow allows you to **feedback** an image using the history.

A classic example when showing the feedback concept is the poor man's [grey scott diffusion model](https://groups.csail.mit.edu/mac/projects/amorphous/GrayScott/) i.e the "creative" derivative using only a gaussian blur and a sharp at each fed steps. 

 
Here is an example workflow of just that.

this is the output:  
<p align=center>
<img width=250 src="https://github.com/melMass/comfy_mtb/assets/7041726/162fb62e-96d4-4843-8902-19d59c536469"/>
</p>

and the workflow:
<p align=center>  
<img width=1000 src="https://github.com/melMass/comfy_mtb/assets/7041726/11257918-86ff-4ddd-8d08-f2a59f7f45a2"/>
</p>

<details><summary>expand here to copy paste this workflow</summary>

```json
{"last_node_id":13,"last_link_id":16,"nodes":[{"id":3,"type":"Get Batch From History (mtb)","pos":[401,280],"size":[315,130],"flags":{},"order":4,"mode":0,"inputs":[{"name":"passthrough_image","type":"IMAGE","link":2,"slot_index":0},{"name":"enable","type":"BOOLEAN","link":16,"widget":{"name":"enable"}}],"outputs":[{"name":"images","type":"IMAGE","links":[8],"shape":3,"slot_index":0}],"properties":{"Node name for S&R":"Get Batch From History (mtb)"},"widgets_values":[false,1,0,357]},{"id":1,"type":"Batch Shape (mtb)","pos":[90,228],"size":[210,310],"flags":{},"order":0,"mode":0,"outputs":[{"name":"IMAGE","type":"IMAGE","links":[2],"shape":3,"slot_index":0}],"properties":{"Node name for S&R":"Batch Shape (mtb)"},"widgets_values":[1,"Box",512,512,229,"#ffffff","#000000","#000000",0,0]},{"id":10,"type":"Blur (mtb)","pos":[733,282],"size":[315,82],"flags":{},"order":6,"mode":0,"inputs":[{"name":"image","type":"IMAGE","link":8}],"outputs":[{"name":"IMAGE","type":"IMAGE","links":[14],"shape":3,"slot_index":0}],"properties":{"Node name for S&R":"Blur (mtb)"},"widgets_values":[8,6]},{"id":13,"type":"Sharpen (mtb)","pos":[1067,280],"size":[315,130],"flags":{},"order":7,"mode":0,"inputs":[{"name":"image","type":"IMAGE","link":14}],"outputs":[{"name":"IMAGE","type":"IMAGE","links":[15],"shape":3,"slot_index":0}],"properties":{"Node name for S&R":"Sharpen (mtb)"},"widgets_values":[31,1,1,1]},{"id":2,"type":"PreviewImage","pos":[1404,278],"size":[210,246],"flags":{},"order":8,"mode":0,"inputs":[{"name":"images","type":"IMAGE","link":15}],"properties":{"Node name for S&R":"PreviewImage"}},{"id":6,"type":"Int To Bool (mtb)","pos":[153,597],"size":[210,42.27488708496094],"flags":{},"order":2,"mode":0,"inputs":[{"name":"int","type":"INT","link":4,"widget":{"name":"int"}}],"outputs":[{"name":"BOOLEAN","type":"BOOLEAN","links":[16],"shape":3,"slot_index":0}],"properties":{"Node name for S&R":"Int To Bool (mtb)"},"widgets_values":[0]},{"id":9,"type":"Get Batch From History (mtb)","pos":[181,706],"size":[315,130],"flags":{},"order":3,"mode":0,"inputs":[{"name":"passthrough_image","type":"IMAGE","link":null,"slot_index":0},{"name":"enable","type":"BOOLEAN","link":6,"widget":{"name":"enable"}}],"outputs":[{"name":"images","type":"IMAGE","links":[7],"shape":3,"slot_index":0}],"properties":{"Node name for S&R":"Get Batch From History (mtb)"},"widgets_values":[true,44,0,357]},{"id":7,"type":"Save Gif (mtb)","pos":[567,703],"size":[210,372],"flags":{},"order":5,"mode":0,"inputs":[{"name":"image","type":"IMAGE","link":7}],"properties":{"Node name for S&R":"Save Gif (mtb)"},"widgets_values":[20,1,false,true,"nearest","/view?filename=25d12cbdb5.gif&subfolder=&type=output"]},{"id":4,"type":"Animation Builder (mtb)","pos":[-110,596],"size":[210,318],"flags":{},"order":1,"mode":0,"outputs":[{"name":"frame","type":"INT","links":[4],"shape":3,"slot_index":0},{"name":"0-1 (scaled)","type":"FLOAT","links":null,"shape":3},{"name":"count","type":"INT","links":null,"shape":3},{"name":"loop_ended","type":"BOOLEAN","links":[6],"shape":3,"slot_index":3}],"properties":{"Node name for S&R":"Animation Builder (mtb)"},"widgets_values":[45,1,1,0,0,"Idle","Iteration: Idle","reset","queue"]}],"links":[[2,1,0,3,0,"IMAGE"],[4,4,0,6,0,"INT"],[6,4,3,9,1,"BOOLEAN"],[7,9,0,7,0,"IMAGE"],[8,3,0,10,0,"IMAGE"],[14,10,0,13,0,"IMAGE"],[15,13,0,2,0,"IMAGE"],[16,6,0,3,1,"BOOLEAN"]],"groups":[],"config":{},"extra":{},"version":0.4}
```

</details>

The blue bordered node is the one doing the feedback, on first frame (frame == 0 converted to bool is false) the passthrough image will be used, this example uses the [Batch Shape](nodes-batch-shape) node, only on the first queue item, then the previous queue item is fed to each subsequent queue item.
The orange bordered one is fetching all the frames we queued once done to assemble the GIF. All this happens in "one click" thanks to [Animation Builder](nodes-animation-builder)


## Inputs
|name|description|
|-|-|
|passthrough_image | This is the image that gets sent out when `enable` is set to false, useful for the init first image in the fake deforum [example](Examples) for instance ([04-animation_builder-deforum.json](https://github.com/melMass/comfy_mtb/blob/main/examples/04-animation_builder-deforum.json)) |
|enable | This makes the node not fetch the history. For instance when you just initiated the server the history is empty, see [Animation Builder](nodes-animation-builder) for practical examples |
|count | the number of frames to fetch from the history |
| **Reset Button** | resets the internal counters, although the node is though around using its queue button it should still work fine when using the regular queue button of comfy |
| **Queue Button** | Convenience button to run the queues (`total_frames` * `loop_count`) |