git clone git://anongit.kde.org/qca.git
cd qca && git archive --format=tar --prefix qca-$(date +%Y%m%d)/ master | xz -9 > ../qca-$(date +%Y%m%d).tar.xz
