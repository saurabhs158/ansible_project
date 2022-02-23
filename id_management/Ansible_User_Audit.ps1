$strComputer = get-content env:computername
#Write-Host "Computer: $strComputer"
$computer = [ADSI]"WinNT://$strComputer"
$objCount = ($computer.psbase.children | measure-object).count
#Write-Host "Q-ty objects for computer '$strComputer' = $objCount"
$Counter = 1
$result = @()
foreach($adsiObj in $computer.psbase.children)
{
  switch -regex($adsiObj.psbase.SchemaClassName)
    {
      "group"
      {
        $group = $adsiObj.name
        $LocalGroup = [ADSI]"WinNT://$strComputer/$group,group"
        $Members = @($LocalGroup.psbase.Invoke("Members"))
        $objCount = ($Members | measure-object).count
        #Write-Host "Q-ty objects for group '$group' = $objCount"
        $GName = $group.tostring()

        ForEach ($Member In $Members) {
          $Name = $Member.GetType().InvokeMember("Name", "GetProperty", $Null, $Member, $Null)
          $Path = $Member.GetType().InvokeMember("ADsPath", "GetProperty", $Null, $Member, $Null)
          #Write-Host " Object = $Path"

                   $isGroup = ($Member.GetType().InvokeMember("Class", "GetProperty", $Null, $Member, $Null) -eq "group")
          If (($Path -like "*/$strComputer/*") -Or ($Path -like "WinNT://NT*")) { $Type = "Local"
          } Else {$Type = "Domain"}

          $Enabled = "-"
          try {
              $Enabled = (Get-LocalUser -Name $Name -ErrorAction Stop).Enabled
          } catch {
              #$_.Exception.Message
          }
          $result += New-Object PSObject -Property @{
            Servername = $strComputer
            UserName = $Name
            UserPath = $Path
            UserType = $Type
            Group = $GName
            isGroupMemeber = $isGroup
            UserEnabled = $Enabled
            Depth = $Counter
          }
        }
      }
    } #end switch
} #end foreach
#Write-Host "Total objects = " ($result | measure-object).count
$date = Get-Date -Format "yyyyMMddhhmm"
$file_path = "C:\Ansible_User_Report-$date.csv"
$result = $result | select-object Servername, Group, UserName, UserType, UserEnabled, UserPath, isGroupMemeber
$result | Export-Csv -path $file_path -Delimiter ";" -Encoding "UTF8" -force -NoTypeInformation
type $file_path
