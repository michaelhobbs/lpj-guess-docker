FROM alpine:3.18.4

WORKDIR /lpj-guess

RUN apk --no-cache add \
  build-base \
  cmake \
  curl
# TODO: NETCDF , and other stuff
RUN curl https://zenodo.org/records/8065737/files/guess_4.1.1.zip?download=1 --output guess.zip
RUN unzip guess.zip
RUN rm guess.zip
WORKDIR /lpj-guess/guess_4.1/build/
RUN cmake ..
RUN make
RUN mkdir ../runs
WORKDIR /lpj-guess/guess_4.1/runs
RUN cp ../data/ins/*.ins .
RUN cp ../data/gridlist/gridlist_global.txt .
RUN ln -s ../build/guess .
RUN echo 'outputdirectory "./out/"' >> ./europe_demo.ins
RUN mkdir out
RUN sed -i 's@tmp30_21.grd@../data/env/tmp30_21.grd@g' europe_demo.ins
RUN sed -i 's@prc30_21.grd@../data/env/prc30_21.grd@g' europe_demo.ins
RUN sed -i 's@clo30_21.grd@../data/env/clo30_21.grd@g' europe_demo.ins
RUN sed -i 's@soils_lpj.dat@../data/env/soils_lpj.dat@g' europe_demo.ins
RUN head -n 1 gridlist_global.txt > gridlist.txt

ENTRYPOINT ["./guess"]
CMD ["-input", "demo", "europe_demo.ins"]