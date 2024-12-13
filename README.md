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
   
<H2>How to use</H2>

### Calculate infected cell image
1. Image upload
   Click on **[File]** - **[Upload Image]** to upload the H&E image.
![1-1](https://github.com/user-attachments/assets/ec70d4c8-dbf3-422a-8790-12431964d738)
![1-2](https://github.com/user-attachments/assets/1fe3837c-ddbc-4db9-80f6-038f605b97ca)

3. Calculate infected cell ratio
   Click the **[Calculate]** button at the bottom left to process the uploaded image.
![2-1](https://github.com/user-attachments/assets/9d7e3ef0-a293-4cc4-b30f-742c292a1b44)
![2-2](https://github.com/user-attachments/assets/38a4b5ea-8e03-4db8-ad33-8c606b08ca51)


4. Crop
   The program also analyze the infection range not only for the entire image but also for specific sections. By clicking **[Crop]** - **[Select]**, you can calculate the infection range for a selected area. Additionally, the cropped image can be reverted to the original image using **[Edit]** - **[Undo]**.
![3](https://github.com/user-attachments/assets/83460900-31c3-4b6c-bf48-372da0d120d6)

<H2>Contact Us</H2>
If you have any questions or provide your cell images, please contact us by email

- Hongseok Oh: [hs.oh-isw@cbnu.ac.kr](mailto:hs.oh-isw@cbnu.ac.kr)
- Jaemine Jeong: [jm.jeong-isw@chungbuk.ac.kr](mailto:jm.jeong-isw@chungbuk.ac.kr)


