<h1>SEPO-IR: Software-based Evaluation PrOcess for calculate Infection Rate</h1>

<H2>Introduction & Features</H2>
This software support pathologists and researchers to provide quantative biomarker assesement throught pixel-based analysis.

- Propose quantitative biomarker assessment through pixel-based analysis.
- Reduce human bias and improve efficiency in labor-intensive tasks using quantitative evaluation.
- Provide the analysis pipeline as an application to ensure ease of use.

### Highlight
![Graphical abstract](https://github.com/user-attachments/assets/f480bcfa-056e-4e40-9e0e-e43b8890c69d)

### Preview
![sample](https://github.com/user-attachments/assets/e26887d4-f10b-479b-80ac-c341462da66e)


<H2>How to run</H2>

1. Virtual environment
   
   1). Create and activate virtual environment
   
   >
   >  **Create**: conda create -n sepo python==3.7
   > 
   >  **Activate**: conda activate seop
   >

   2). Install python packages with requirements.txt 

   > **Requirements**: pip install -r requirements.txt
   
   3). Run SEPI_IR

   > **Run**: python main.py
   
3. Executable file
   1). Download project
   2). Unzip "SEPO_IR.exe.zip"
   3). Execute "SEPO-IR.exe"
   
<H2>How to Use</H2>

### Calculate infected cell image
1. Image upload
   Click on [File] - [Upload Image] to upload the H&E image.

3. Calculate infected cell ratio
   Click the [Calculate] button at the bottom left to process the uploaded image.

4. Crop
   The program also analyze the infection range not only for the entire image but also for specific sections. By clicking [Crop], you can calculate the infection range for a selected area. Additionally, the cropped image can be reverted to the original image using [Edit] - [Undo].


<H2>Contact Us</H2>
If you have any questions or provide your cell images, please contact us by email

- Hongseok Oh: [hs.oh-isw@cbnu.ac.kr](mailto:hs.oh-isw@cbnu.ac.kr)
- Jaemine Jeong: [jm.jeong-isw@chungbuk.ac.kr](mailto:jm.jeong-isw@chungbuk.ac.kr)


