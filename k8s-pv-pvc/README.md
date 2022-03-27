# StorageClass
- `retainPolicy`: Control pv behavior when pvc been deleted
- StorageClass object must be valid DNS subdomain name.
- [`volumeBindingMode`](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode): controls when volume binding and dynamic provisioning should occur. When unset, "Immediate" mode is used by default.

# [Persistent Volume Claim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)  
- [Official Document#Protection](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#storage-object-in-use-protection)
> If a user deletes a PVC in active use by a Pod, the PVC is not removed immediately. PVC removal is postponed until the PVC is no longer actively used by any Pods

# Useful links
- [CSI 基本介紹](https://www.hwchiu.com/csi.html)
- [K8s Storage 1](https://www.hwchiu.com/kubernetes-storage-i.html)
