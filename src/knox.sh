echo "Disabling encryption"
for fstab in "$WORK_DIR"/vendor/etc/fstab.exynos* "$WORK_DIR"/vendor/etc/fstab.qcom*; do
    [ -f "$fstab" ] && sed -i 's/,fileencryption=ice//g' "$fstab"
done

echo "Disabling vaultkeeper"
rm -f "$WORK_DIR/vendor/bin/vaultkeeperd"
rm -f "$WORK_DIR/vendor/bin/vendor.samsung.hardware.security.vaultkeeper@2.0-service"
rm -f "$WORK_DIR/vendor/etc/init/vaultkeeper_common.rc"
rm -f "$WORK_DIR/vendor/etc/vintf/manifest/vaultkeeper_manifest.xml"

echo "Disabling cass"
rm -f "$WORK_DIR/vendor/bin/cass"
rm -f "$WORK_DIR/vendor/etc/init/cass.rc"

echo "Disabling proca"
rm -f "$WORK_DIR/vendor/bin/vendor.samsung.hardware.security.proca@2.0-service"
rm -f "$WORK_DIR/vendor/etc/init/pa_daemon_teegris.rc"

echo "Disabling wsm"
rm -f "$WORK_DIR/vendor/bin/vendor.samsung.hardware.security.wsm@1.0-service"
rm -f "$WORK_DIR/vendor/etc/init/wsm-service.rc"
sed -i -e '/<hal format="hidl">/{N;/<name>vendor\.samsung\.hardware\.security\.wsm<\/name>/{:loop;N;/<\/hal>/!bloop;d}}' "$WORK_DIR/vendor/etc/vintf/manifest.xml"

echo "Disabling recovery restoration"
rm -f "$WORK_DIR/vendor/recovery-from-boot.p"
rm -f "$WORK_DIR/vendor/bin/install-recovery.sh"
rm -f "$WORK_DIR/vendor/etc/init/vendor_flash_recovery.rc"

echo "Disabling KnoxGuard"
rm -f "$WORK_DIR/vendor/bin/hw/vendor.samsung.hardware.tlc.iccc@1.0-service"
rm -f "$WORK_DIR/vendor/etc/init/vendor.samsung.hardware.tlc.iccc@1.0-service.rc"
rm -f "$WORK_DIR/vendor/etc/vintf/manifest/vendor.samsung.hardware.tlc.iccc@1.0-manifest.xml"

echo "Disabling Defex policy"
rm -f "$WORK_DIR/system/dpolicy_system"
rm -f "$WORK_DIR/vendor/etc/dpolicy"

if [[ $TARGET_API_LEVEL -lt 34 ]]; then
    echo "Disabling fabric crypto"
    rm -f "$WORK_DIR/system/system/bin/fabric_crypto"
    rm -f "$WORK_DIR/system/system/etc/init/fabric_crypto.rc"
    rm -f "$WORK_DIR/system/system/etc/permissions/FabricCryptoLib.xml"
    rm -f "$WORK_DIR/system/system/etc/permissions/privapp-permissions-com.samsung.android.kmxservice.xml"
    rm -f "$WORK_DIR/system/system/etc/vintf/manifest/fabric_crypto_manifest.xml"
    rm -f "$WORK_DIR/system/system/framework/FabricCryptoLib.jar"
    rm -f "$WORK_DIR/system/system/lib64/com.samsung.security.fabric.cryptod-V1-cpp.so"
    rm -f "$WORK_DIR/system/system/lib64/vendor.samsung.hardware.security.fkeymaster-V1-cpp.so"
    rm -f "$WORK_DIR/system/system/lib64/vendor.samsung.hardware.security.fkeymaster-V1-ndk.so"
    rm -rf "$WORK_DIR/system/system/priv-app/KmxService"
    sed -i -e '/<hal format="aidl" optional="true">/{N;/<name>vendor\.samsung\.hardware\.security\.fkeymaster<\/name>/{:loop;N;/<\/hal>/!bloop;d}}' "$WORK_DIR/system/system/etc/vintf/compatibility_matrix.device.xml"
fi