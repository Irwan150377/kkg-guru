"""
Cloudinary Configuration untuk File Upload
"""
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

def init_cloudinary():
    """Initialize Cloudinary dengan credentials dari environment variables"""
    cloudinary.config(
        cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
        api_key=os.environ.get("CLOUDINARY_API_KEY"),
        api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
        secure=True
    )

def upload_file(file, folder="kkg_guru"):
    """
    Upload file ke Cloudinary
    
    Args:
        file: File object dari Flask request.files
        folder: Folder di Cloudinary (default: kkg_guru)
    
    Returns:
        dict: Response dari Cloudinary dengan url, public_id, dll
    """
    try:
        # Upload ke Cloudinary dengan auto resource type detection
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="auto",  # Auto detect: image, video, raw (untuk PDF, DOC, dll)
            use_filename=True,
            unique_filename=True,
            overwrite=False
        )
        return {
            "success": True,
            "url": result.get("secure_url"),
            "public_id": result.get("public_id"),
            "format": result.get("format"),
            "resource_type": result.get("resource_type"),
            "bytes": result.get("bytes")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def delete_file(public_id, resource_type="raw"):
    """
    Hapus file dari Cloudinary
    
    Args:
        public_id: Public ID dari file di Cloudinary
        resource_type: Type of resource (image, video, raw)
    
    Returns:
        dict: Response dari Cloudinary
    """
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return {
            "success": result.get("result") == "ok",
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_file_url(public_id, resource_type="raw"):
    """
    Generate URL untuk file di Cloudinary
    
    Args:
        public_id: Public ID dari file
        resource_type: Type of resource
    
    Returns:
        str: Secure URL untuk download file
    """
    return cloudinary.CloudinaryResource(public_id, resource_type=resource_type).url

def is_cloudinary_configured():
    """Check apakah Cloudinary sudah dikonfigurasi"""
    return all([
        os.environ.get("CLOUDINARY_CLOUD_NAME"),
        os.environ.get("CLOUDINARY_API_KEY"),
        os.environ.get("CLOUDINARY_API_SECRET")
    ])
