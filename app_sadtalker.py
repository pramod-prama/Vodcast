import os, sys
import gradio as gr
from src.gradio_demo import SadTalker  


try:
    import webui  # in webui
    in_webui = True
except:
    in_webui = False


def toggle_audio_file(choice):
    if choice == False:
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)
    
def ref_video_fn(path_of_ref_video):
    if path_of_ref_video is not None:
        return gr.update(value=True)
    else:
        return gr.update(value=False)

def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):

    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    with gr.Blocks(analytics_enabled=False) as sadtalker_interface:
        gr.Markdown("<div align='center'> <h2> 😭 SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation (CVPR 2023) </span> </h2> \
                    <a style='font-size:18px;color: #efefef' href='https://arxiv.org/abs/2211.12194'>Arxiv</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                    <a style='font-size:18px;color: #efefef' href='https://sadtalker.github.io'>Homepage</a>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                     <a style='font-size:18px;color: #efefef' href='https://github.com/Winfredy/SadTalker'> Github </div>")
        
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('Upload image'):
                        with gr.Row():
                            source_image = gr.Image(label="Source image", source="upload", type="filepath", elem_id="img2img_image").style(width=512)

                with gr.Tabs(elem_id="sadtalker_driven_audio"):
                    with gr.TabItem('Upload OR TTS'):
                        with gr.Column(variant='panel'):
                            driven_audio = gr.Audio(label="Input audio", source="upload", type="filepath")

                        if sys.platform != 'win32' and not in_webui: 
                            from src.utils.text2speech import TTSTalker
                            tts_talker = TTSTalker()
                            with gr.Column(variant='panel'):
                                input_text = gr.Textbox(label="Generating audio from text", lines=5, placeholder="please enter some text here, we genreate the audio from text using @Coqui.ai TTS.")
                                tts = gr.Button('Generate audio',elem_id="sadtalker_audio_generate", variant='primary')
                                tts.click(fn=tts_talker.test, inputs=[input_text], outputs=[driven_audio])
                            
            with gr.Column(variant='panel'): 
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('Settings'):
                        gr.Markdown("need help? please visit our [best practice page](https://github.com/OpenTalker/SadTalker/blob/main/docs/best_practice.md) for more detials")
                        with gr.Column(variant='panel'):
                            # width = gr.Slider(minimum=64, elem_id="img2img_width", maximum=2048, step=8, label="Manually Crop Width", value=512) # img2img_width
                            # height = gr.Slider(minimum=64, elem_id="img2img_height", maximum=2048, step=8, label="Manually Crop Height", value=512) # img2img_width
                            pose_style = gr.Slider(minimum=0, maximum=46, step=1, label="Pose style", value=0) # 
                            size_of_image = gr.Radio([256, 512], value=256, label='face model resolution', info="use 256/512 model?") # 
                            preprocess_type = gr.Radio(['crop', 'resize','full', 'extcrop', 'extfull'], value='crop', label='preprocess', info="How to handle input image?")
                            is_still_mode = gr.Checkbox(label="Still Mode (fewer head motion, works with preprocess `full`)")
                            batch_size = gr.Slider(label="batch size in generation", step=1, maximum=10, value=2)
                            enhancer = gr.Checkbox(label="GFPGAN as Face enhancer")
                            submit = gr.Button('Generate', elem_id="sadtalker_generate", variant='primary')
                            
                with gr.Tabs(elem_id="sadtalker_genearted"):
                        gen_video = gr.Video(label="Generated video", format="mp4").style(width=256)

        if warpfn:
            submit.click(
                        fn=warpfn(sad_talker.test), 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[gen_video]
                        )
        else:
            submit.click(
                        fn=sad_talker.test, 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[gen_video]
                        )

    return sadtalker_interface
 

if __name__ == "__main__":
    # Build Gradio UI
    demo = sadtalker_demo()

    # Expose a clean FastAPI endpoint for Postman/clients
    try:
        from uuid import uuid4
        from fastapi import File, UploadFile, Form
        from fastapi.responses import JSONResponse
        from fastapi.exceptions import RequestValidationError
        from fastapi import Request
        from starlette.exceptions import HTTPException as StarletteHTTPException

        app = demo.app

        @app.exception_handler(RequestValidationError)
        async def gradio_validation_exception_handler(request: Request, exc: RequestValidationError):
            # Avoid UTF-8 decode of potential binary by stringifying the error only
            return JSONResponse(status_code=422, content={
                "status": "error",
                "message": str(exc)
            })

        @app.exception_handler(StarletteHTTPException)
        async def gradio_http_exception_handler(request: Request, exc: StarletteHTTPException):
            return JSONResponse(status_code=exc.status_code, content={
                "status": "error",
                "message": str(exc.detail)
            })

        @app.exception_handler(Exception)
        async def gradio_generic_exception_handler(request: Request, exc: Exception):
            return JSONResponse(status_code=500, content={
                "status": "error",
                "message": str(exc)
            })

        @app.post("/api/generate")
        async def api_generate(
            source_image: UploadFile = File(...),
            driven_audio: UploadFile = File(...),
            preprocess: str = Form("crop"),
            still_mode: bool = Form(False),
            use_enhancer: bool = Form(False),
            batch_size: int = Form(1),
            size: int = Form(256),
            pose_style: int = Form(0),
        ):
            try:
                tag = str(uuid4())
                base_dir = os.path.join("results", tag)
                input_dir = os.path.join(base_dir, "input")
                os.makedirs(input_dir, exist_ok=True)

                # Save uploads
                src_path = os.path.join(input_dir, source_image.filename)
                with open(src_path, "wb") as f:
                    f.write(await source_image.read())

                aud_path = os.path.join(input_dir, driven_audio.filename)
                with open(aud_path, "wb") as f:
                    f.write(await driven_audio.read())

                # Run SadTalker
                sad_talker = SadTalker("checkpoints", "src/config", lazy_load=True)
                output_path = sad_talker.test(
                    source_image=src_path,
                    driven_audio=aud_path,
                    preprocess=preprocess,
                    is_still_mode=still_mode if "is_still_mode" in SadTalker.test.__code__.co_varnames else False,
                    still_mode=still_mode,
                    use_enhancer=use_enhancer,
                    batch_size=batch_size,
                    size=size,
                    pose_style=pose_style,
                    result_dir=base_dir,  # keep result in same folder
                )

                # Ensure output_path is a string (filepath)
                if isinstance(output_path, bytes):
                    fixed_path = os.path.join(base_dir, "result.mp4")
                    with open(fixed_path, "wb") as f:
                        f.write(output_path)
                    output_path = fixed_path

                output_path = str(output_path)

                return JSONResponse({
                    "status": "ok",
                    "video_path": output_path,   # path on server
                    "result_id": tag
                })
            except Exception as e:
                return JSONResponse({
                    "status": "error",
                    "message": str(e)
                }, status_code=500)
    except Exception as _:
        # If FastAPI is unavailable for any reason, continue with UI only
        pass

    demo.queue()
    demo.launch()


