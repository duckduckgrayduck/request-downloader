"""
This Add-On uploads files from a MuckRock request to
a  project on your DocumentCloud
"""
import sys
from muckrock import MuckRock
from documentcloud.addon import AddOn



class MuckRockExporter(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""
        # fetch your add-on specific data
        project_name = self.data.get("project_name")
        request_id = self.data.get("request_id")

        self.set_message(f"Fetching files from MuckRock request {request_id}")
        mr_client = MuckRock()

        request = mr_client.requests.retrieve(request_id)

        # Retrieves all of the communications from the request
        comms_list = request.get_communications()

        all_files = []

        # For each communication, if there is an attached file, add the file to a list.
        for comm in comms_list:
            files = list(comm.get_files())
            if files:  # Filters out comms with no actual files
                all_files.extend(files)

        # Build out a list of file URLs we can use to upload to DocumentCloud
        file_urls = []
        for file in all_files:
            file_urls.append(file.ffile)

        try:
            project = self.client.projects.create(project_name)
        except Exception as e:
            self.set_message("Failed to create a project, check Github logs")
            print(e)
            sys.exit(1)
        self.set_message("Uploading the documents to DocumentCloud")
        try:
            self.client.documents.upload_urls(file_urls, projects=[project.id])
            self.set_message("Successfully uploaded all documents to DocumentCloud")
        except Exception as e:
            print(e)
            self.set_message("Failed to upload documents to DocumentCloud, check Github logs")
            sys.exit(1)


if __name__ == "__main__":
    MuckRockExporter().main()
