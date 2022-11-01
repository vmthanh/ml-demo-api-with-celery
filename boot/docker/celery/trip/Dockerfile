
ARG VM_BASE
FROM $VM_BASE

ARG VM_USER
ARG VM_HOME
ARG VM_CODE
ARG VM_CONDA

RUN apt-get update --fix-missing \
  && apt-get install --fix-missing -y \
  bzip2 \
  libgtk2.0-dev \
  sudo \
  wget \
  && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' $VM_USER \
  && adduser $VM_USER sudo \
  && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
  && chown -R $VM_USER $VM_HOME

USER $VM_USER

WORKDIR $VM_HOME/
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
  && bash miniconda.sh -b -p $VM_HOME/miniconda \
  && rm miniconda.sh
ENV PATH $VM_HOME/miniconda/bin:$PATH

WORKDIR $VM_HOME/
COPY $VM_CONDA ./venv.yml
#RUN conda update -n base -c defaults conda \
# && conda env create -n venv -f ./venv.yml \
# && conda clean -y --all
RUN conda env create -n venv -f ./venv.yml \
  && conda clean -y --all

COPY . $VM_CODE
# WORKDIR $VM_CODE/repo
WORKDIR $VM_CODE/
ENTRYPOINT ["boot/docker/celery/trip/entrypoint.sh"]
