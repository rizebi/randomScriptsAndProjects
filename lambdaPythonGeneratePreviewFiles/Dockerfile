FROM amazon/aws-lambda-python:3.8

# Update the system
RUN yum -y update

# Install dependencies
RUN yum install -y python3 pip wget tar exiftool imagemagick zlib1g-dev libjpeg-dev python3-pythonmagick inkscape xvfb poppler-utils libfile-mimeinfo-perl qpdf libimage-exiftool-perl ffmpeg

# Install pachage that actually does the previews
RUN pip install preview-generator boto3

# Install libreoffice (needed for generating previews form PDF, Word, Excel, etc.)
# Note that this version of libreoffice might not be available in the future. To rebuild the image, change the url path, and the symbolic link source
RUN mkdir /tmp/libreoffice; cd libreoffice; wget https://download.documentfoundation.org/libreoffice/stable/7.1.3/rpm/x86_64/LibreOffice_7.1.3_Linux_x86-64_rpm.tar.gz; tar -xvf LibreOffice_*_Linux_x86-64_rpm.tar.gz; cd LibreOffice_*_Linux_x86-64_rpm; cd RPMS; yum -y localinstall *.rpm; rm -rf /tmp/libreoffice; ln -sfn /usr/bin/libreoffice7.1 /usr/bin/libreoffice

# Copy lambda function code
COPY lambda_function.py ./

CMD [ "lambda_function.lambda_handler" ]