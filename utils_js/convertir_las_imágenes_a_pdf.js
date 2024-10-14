const { Builder, By, until } = require('selenium-webdriver');
const path = require('path');
const fs = require('fs');

async function convertirImagenesAPdf(images, serie, chapter) {
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // Navegar a la página de conversión de imágenes a PDF
        await driver.get('https://bigpdf.11zon.com/en/images-to-pdf/');

        // Subir las imágenes
        let selectImageButton = await driver.findElement(By.css('.btn.big_select_btn'));
        let inputFileElement = await driver.findElement(By.css('input[type="file"]'));

        // Convertir las rutas de las imágenes a rutas absolutas
        let imagePaths = images.map(image => path.resolve(image));

        // Simular la subida de imágenes al input de tipo file
        await inputFileElement.sendKeys(imagePaths.join('\n'));

        // Esperar que las imágenes se hayan subido (puedes ajustar el tiempo de espera según el número de imágenes)
        await driver.wait(until.elementLocated(By.id('zon-right-btn-text')), 30000);

        // Seleccionar los parámetros de conversión
        let pageSizeDropdown = await driver.findElement(By.id('select-pageSize'));
        await pageSizeDropdown.sendKeys('Fit (As image size)');  // Seleccionar "Fit As Image Size"

        let qualityDropdown = await driver.findElement(By.id('select-img-quality'));
        await qualityDropdown.sendKeys('Same As Image (100%)');  // Seleccionar calidad 100%

        // Convertir las imágenes a PDF
        let convertButton = await driver.findElement(By.id('zon-right-btn'));
        await convertButton.click();

        // Esperar a que el botón de descarga esté disponible
        await driver.wait(until.elementLocated(By.id('zon-download-file')), 60000);  // Puede tardar más dependiendo del tamaño de las imágenes

        // Descargar el PDF
        let downloadButton = await driver.findElement(By.id('zon-download-file'));
        let downloadLink = await downloadButton.getAttribute('href');

        // Descargar el archivo PDF desde el link
        let pdfFileName = `${serie}_${chapter}.pdf`;
        let downloadPath = path.join(__dirname, pdfFileName);

        let file = fs.createWriteStream(downloadPath);
        https.get(downloadLink, function (response) {
            response.pipe(file);
            file.on('finish', function () {
                file.close();
                console.log(`PDF descargado y guardado como ${pdfFileName}`);
            });
        });

    } finally {
        // Cerrar el navegador
        await driver.quit();
    }
}

// Ejemplo de uso (debes pasar un array de rutas de imágenes):
convertirImagenesAPdf(['ruta/a/imagen1.jpg', 'ruta/a/imagen2.jpg'], 'nombre_serie', 1);
