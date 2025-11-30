# Maintainer: Daniel Seichter <daniel.seichter@dseichter.de>
pkgname=yahac
pkgver=0.4.0
pkgrel=1
pkgdesc="Yet Another Home Assistant Client - Desktop tray application for Home Assistant"
arch=('x86_64')
url="https://github.com/dseichter/yahac"
license=('GPL3')
options=('!debug')
depends=('python-pyside6' 'python-urllib3' 'python-paho-mqtt')
optdepends=('libnotify: Desktop notifications')
makedepends=('python-build' 'python-installer' 'python-wheel')
source=("$pkgname-$pkgver.tar.gz::https://github.com/dseichter/yahac/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    
    # Install main script
    install -Dm755 src/yahac.py "$pkgdir/usr/bin/yahac"
    
    # Install desktop file
    install -Dm644 debian/yahac.desktop "$pkgdir/usr/share/applications/yahac.desktop"
    
    # Install documentation
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}